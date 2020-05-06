base_connection_string <- "jdbc:snowflake://cengage.snowflakecomputing.com/?account=cengage&user=%s&password=%s&db=dev&schema=datamining&tracing=OFF&role=ANALYST"
Connection_string <- sprintf(base_connection_string,"shweta.purushe@cengage.com","Sanatsadhale2017")


jdbcDriver <- JDBC(driverClass="com.snowflake.client.jdbc.SnowflakeDriver", classPath="/Library/Java/Extensions/snowflake-jdbc-3.5.5.jar")
jdbcConnection <- dbConnect(jdbcDriver, Connection_string)

dbGetQuery(jdbcConnection, "use warehouse analysis");
dbGetQuery(jdbcConnection, "use role datascience");

query <- "with cu_starters as (
      select
          user_sso_guid
          ,subscription_start 
          ,subscription_state
          ,lead(subscription_state, 1) OVER (PARTITION BY user_sso_guid ORDER BY local_time) IS NULL AS latest
      from prod.unlimited.raw_subscription_event
      where subscription_state in ('trial_access', 'full_access')  
  )  
  ,trial_users as (
      select 
          user_sso_guid
          ,subscription_start date_2
          ,subscription_state
      from cu_starters
      where latest = 'FALSE' --704189   -- people with latest = TRUE are direct subscribers and should be excluded from study --2104790
  )
  select 
      datediff(days, date_2, subscription_start) as Rel_Day_Of_Trial
      ,cu_starters.subscription_state
      ,count(*) count
  from cu_starters inner join trial_users on cu_starters.user_sso_guid = trial_users.user_sso_guid
  group by 1, 2
;"

df <- dbGetQuery(jdbcConnection, query)


df %>% filter(REL_DAY_OF_TRIAL > -10 & REL_DAY_OF_TRIAL < 14) %>%
ggplot(aes(x=REL_DAY_OF_TRIAL, y=COUNT))+geom_bar(stat = "identity") + facet_grid(~SUBSCRIPTION_STATE)


df %>% filter(REL_DAY_OF_TRIAL > -10 & REL_DAY_OF_TRIAL < 14) %>%
ggplot(aes(REL_DAY_OF_TRIAL, COUNT))+geom_bar(aes(fill=SUBSCRIPTION_STATE), stat = "identity")

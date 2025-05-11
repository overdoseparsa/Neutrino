# Secure Option 
# 1) Have  to disable and have altration from django filter such as 

```bash 
curl /account/3/?id=3 
{
"Response":"account3"
}
curl /account/3/id=4/ 
{
"Response":"account4"
}
```
### it It does not mean we want to just use id 
we have to be care  that Simple cilent dont access Directly to the database  match query 

# java-to-json
A sublime text 3 plugin to convert Java field definitions into a sample json message

# Usage 
Can be invoked through Command Pallete (Cmd+Shift+P) by invoking the `j2j` command

### example
input: 
``` 
 @JsonProperty("identified")
 private Long id;
 
 @JsonProperty("honorific")
 private String title;
 
 @JsonProperty("targetUrl")
 private String url;
 
 private String date;
 
 private String userName;
 ```



output:

```
{
  "date": "date",
  "id": "id",
  "title": "title",
  "url": "url",
  "userName": "userName"
}
```


# java-to-json
A sublime text 3 plugin to convert Java field definitions into a sample json message

# Usage 
Can be invoked through Command Pallete (Cmd+Shift+P) by invoking the `j2j` command

### example
input: 
``` 
package org.example;

import lombok.Data;

@Data
public class MyClass
{
    private final String customerId;
    private final Long webId;
    private final String isoCode;
    private final String serialNumber;
    private final Date purchaseDate;
    private final Boolean channel;
}

 ```



output:

```
{
  "channel": true,
  "customerId": "test_value",
  "isoCode": "test_value",
  "purchaseDate": "01-01-2010",
  "serialNumber": "test_value",
  "webId": 9999999
}
```


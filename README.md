# OAuthv1 - Signing (Burp Extension)

## Description


The purpose of this extension is to provide an additional authentication method that is not natively supported by Burp Suite. 
Currently, this tool only supports OAuth v1.


## Issues and Enhancements

Use the Issues tab above to report any problems or enhancement requests.

Current known issues are as follows:

 ~~• No ability to disable entries.~~
  
 ~~• Boolean value in Table is not represented as Checkbox.~~
 
## Usage/Examples

```javascript
To Install Manually:

git clone https://github.com/L1GH7/OAuthv1---Signing-Burp-Extension-.git
Open Burp
Navigate to Extender
Click 'Add'
Change 'Extension Type' to Python
Select the 'PlatformAuthenticationExtended.py' file
Click 'Next' and the Extension should load successfully

To Use:

Navigate to the Platform Authentication Tab
Click 'Add' 
Set your Destination Host to the domain ONLY
Destination Host: Example.com
Authentication Type: OAuth v1 
Consumer Key: <CONSUMER KEY>
Consumer Secret: <CONSUMER SECRET>
Click 'Ok' 
You should see your new entry in the table
By default, your new entry will be enabled automatically 
Currently, there's no way to disable an entry. Just remove it by selecting the row and click 'Remove'
If you want to keep this entry but disable it, you can boolean value to false through the platformAuthentication.json file
```





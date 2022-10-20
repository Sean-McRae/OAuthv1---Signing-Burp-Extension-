# Platform Authentication Extended

## Description


The purpose of this extension is to provide additional authentication methods that are not natively supported by Burp Suite. 
Currently, this tool only supports OAuth v1 but will eventually include AWS Signing (Signature Version 4).


## Issues and Enhancements

Use the Issues tab above to report any problems or enhancement requests.

Current known issues are as follows:

 • Supplied URL parameters are not signed properly thus resulting in a invalid signature.
 
 • No ability to disable entries.
 
 • Table is editable by dbl click but does not change actual data.
 
 • Boolean value in Table is not representated as Checkbox.
 
## Usage/Examples

```javascript
To Install:

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
Username: <CONSUMER KEY>
Password: <CONSUMER SECRET>
Click 'Ok' 
You should see your new entry in the table
By default, your new entry will be enabled automatically 
Currently, there's no way to disable an entry. Just remove it by select the row and clicking 'Remove'
If you want to keep this entry but disable it, you can boolean value to false through the platformAuthentication.json file
```





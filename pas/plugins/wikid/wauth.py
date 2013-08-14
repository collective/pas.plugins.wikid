# Ping
PING = """<transaction>
            <type>0</type>
            <data>
              <value>TX</value>
            </data>
          </transaction>"""

# Connect
CONNECT = """<transaction>
               <type>1</type>
               <data>
                 <client-string>%(client)s</client-string>
                 <server-string>null</server-string>
                 <result>null</result>
               </data>
             </transaction>"""

# Online/Offline Login
# offline login: format - offline
# online login: format - base
#               offline_challenge - null
#               offline_response - null
LOGIN = """ <transaction>
              <type format="%(format)s">2</type>
              <data>
                <user-id>%(user)s</user-id>
                <passcode>%(passcode)s</passcode>
                <domaincode>%(domaincode)s</domaincode>
                <offline-challenge encoding="none">%(challenge)s</offline-challenge>
                <offline-response encoding="none">%(response)s</offline-response>
                <chap-password encoding="base64">%(chap_password)s</chap-password>
                <chap-challenge encoding="base64">%(chap_challenge)s</chap-challenge>
                <result>null</result>
              </data>
            </transaction>"""


# registration in group: groupName - name
# registration outside group: groupName - null
REGISTRATION = """<transaction>
                    <type format="%(format)s">4</type>
                    <data>
                      <user-id>%(user)s</user-id>
                      <registration-code>%(regcode)s</registration-code>
                      <domaincode>%(domaincode)s</domaincode>
                      <passcode>null</passcode>
                      <error-code>null</error-code>
                      <groupName>%(group)s</groupName>
                      <result>null</result>
                    </data>
                 </transaction>"""

#Find user by name
FIND_USER = """<transaction>
                  <type>5</type>
                  <data>
                    <domaincode>%(domaincode)s</domaincode>
                    <user-id>%(user)s</user-id>
                    <result>null</result>
                    <return-code>%(returncode)s</return-code>
                  </data>
                </transaction>"""

# Update user
UPDATE = """<transaction>
              <type>6</type>
              <data>
                <user>
                  <user-id>%(user)s</user-id>
                  <id_usermap>4</id_usermap>
                  <bad-passcode-attempts>0</bad-passcode-attempts>
                  <creation format="ms">1299214800000</creation>
                  <domaincode>%(domaincode)s</domaincode>
                  <status>1</status><token-list>
                  <token>
                      <device-id>%(device_id)s</device-id>
                      <domain-id>%(domain_id)s</domain-id>
                      <offline-public-key encoding="base64">%(offline_pub_key)s</offline-public-key>
                      <status>1</status>
                      <bad-pin-attempts>0</bad-pin-attempts>
                      <offline-authentication-count>0</offline-authentication-count>
                      <creation format="ms">1299214800000</creation>
                      <changed>false</changed>
                      <forDeletion>false</forDeletion>
                      <id_devicemap>6</id_devicemap>
                  </token>
                  </token-list>
                  </user>
                <result>null</result>
                <return-code>%(returncode)s</return-code>
              </data>
            </transaction>"""

# Delete user
DELETE = """<transaction>
              <type>7</type>
              <data>
                <user>
                    <user-id>api</user-id>
                    <id_usermap>4</id_usermap>
                    <bad-passcode-attempts>0</bad-passcode-attempts>
                    <creation format="ms">1299214800000</creation>
                    <domaincode>%(domaincode)s</domaincode>
                    <status>1</status>
                    <token-list>
                       <token>
                       <device-id>%(device_id)s</device-id>
                       <domain-id>%(domain_id)s</domain-id>
                       <offline-public-key encoding="base64">%(offline_pub_key)s</offline-public-key>
                       <status>1</status>
                       <bad-pin-attempts>0</bad-pin-attempts>
                       <offline-authentication-count>0</offline-authentication-count>
                       <creation format="ms">1299214800000</creation>
                       <changed>false</changed>
                       <forDeletion>false</forDeletion>
                       <id_devicemap>6</id_devicemap>
                       </token>
                    </token-list>
                </user>
                <result>null</result>
                <return-code>%(returncode)s</return-code>
              </data>
            </transaction>"""

# Pre-Registration
PRE_REGISTRATION = """<transaction>
                        <type>10</type>
                        <data>
                          <token-registration-code>%(regtoken)s</token-registration-code>
                          <pre-registration-code>%(pre_registration_code)s</pre-registration-code>
                          <domaincode>%(domaincode)s</domaincode>
                          <error-code>null</error-code>
                          <result>null</result>
                        </data>
                      </transaction> """

# Generate a User report
USER_REPORT = """<transaction>
                   <type>12</type>
                   <data dataType="USER" separator=",">
                   <options>
                     <includeDisabledUsers>true</includeDisabledUsers>
                     <includeTokenData>true</includeTokenData>
                     <groupUserData>false</groupUserData>
                     <includeDisabledDevices>false</includeDisabledDevices>
                     <includeUnregistered>false</includeUnregistered>
                   </options>
                   </data>
                 </transaction>"""

# List users in a domain
LIST_USERS = """<transaction>
                    <type>14</type>
                    <data>
                        <domaincode>%(domaincode)s</domaincode>
                        <user-list></user-list>
                    </data>
                </transaction>"""

# List registration codes
LIST_REGCODES = """<transaction>
                     <type>15</type>
                     <data>
                       <regCodeList />
                     </data>
                   </transaction>"""

# TODO:
    # Add device without passcode
    # Test an invalid transaction
    # Add pre-registration
    # Generate a Device/Token report
    # Delete by Device/Token


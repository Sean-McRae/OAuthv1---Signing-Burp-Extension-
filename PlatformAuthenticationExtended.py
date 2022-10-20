from burp import IBurpExtender, IHttpListener
from burp import ITab
from javax.swing import JScrollPane, JTable, JPanel, JTextField, \
    JLabel, JComboBox, JButton, table, BorderFactory, JFrame
from java.awt import Color, GridBagConstraints, GridBagLayout, Insets, \
    Dimension
from javax.swing.table import DefaultTableModel
from createSignature import *
import re

class TableModel(DefaultTableModel):

    def isCellEditable(self, *args):
        return False

class BurpExtender(IBurpExtender, ITab, IHttpListener):

    def getTabCaption(self):
        return 'OAuthv1 - Signing'

    def getUiComponent(self):
        panel = JPanel()
        jScrollPane = JScrollPane()

        def addCredentials(event):
            frame = JFrame('Add Platform Authentication Credentials')
            frame.setSize(900, 600)
            frameLayout = GridBagLayout()
            frame.setLayout(frameLayout)
            gbc = GridBagConstraints()
            gbc.insets = Insets(3, 3, 3, 3)
            destinationHost = JTextField(30)
            destinationHostJLabel = JLabel('Destination Host: ')
            authenticationTypes = ['OAuth v1']
            authenticationType = JComboBox(authenticationTypes)
            authenticationTypeJLabel = JLabel('Authentication Type: ')
            usernameField = JTextField(30)
            usernameFieldJLabel = JLabel('Username: ')
            passwordField = JTextField(30)
            passwordFieldJLabel = JLabel('Password: ')

            def saveNewEntry(event):
                Host = destinationHost.getText()
                Type = authenticationType.getSelectedItem()
                Username = usernameField.getText()
                Password = passwordField.getText()
                appendNewCredentials(Host, Type, Username, Password)
                refreshDataTable()
                frame.dispose()

            def cancelEntryFrame(event):
                frame.dispose()

            saveEntry = JButton('Ok', actionPerformed=saveNewEntry)
            cancelEntry = JButton('Cancel',
                                  actionPerformed=cancelEntryFrame)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 0
            frame.add(destinationHostJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 0
            frame.add(destinationHost, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 1
            frame.add(authenticationTypeJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 1
            frame.add(authenticationType, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 2
            frame.add(usernameFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 2
            frame.add(usernameField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 3
            frame.add(passwordFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 3
            frame.add(passwordField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridwidth = 1
            gbc.gridx = 1
            gbc.gridy = 4
            frame.add(saveEntry, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridwidth = 1
            gbc.gridx = 2
            gbc.gridy = 4
            frame.add(cancelEntry, gbc)
            frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
            frame.setLocationRelativeTo(None)
            frame.setVisible(True)

        def editCredentials(event):
            import json
            frame = JFrame('Edit Platform Authentication Credentials')
            frame.setSize(900, 600)
            frameLayout = GridBagLayout()
            frame.setLayout(frameLayout)
            gbc = GridBagConstraints()
            gbc.insets = Insets(3, 3, 3, 3)
            destinationHost = JTextField(30)
            destinationHostJLabel = JLabel('Destination Host: ')
            authenticationTypes = ['OAuth v1']
            authenticationType = JComboBox(authenticationTypes)
            authenticationTypeJLabel = JLabel('Authentication Type: ')
            usernameField = JTextField(30)
            usernameFieldJLabel = JLabel('Username: ')
            passwordField = JTextField(30)
            passwordFieldJLabel = JLabel('Password: ')
            file_path = 'platformAuthentication.json'
            with open(file_path) as f:
                platformJSON = json.load(f)
            selectedObject = myTable.getSelectedRow()
            destinationHost.setText(platformJSON[selectedObject]['Destination Host'
                                    ])
            usernameField.setText(platformJSON[selectedObject]['Username'
                                  ])
            passwordField.setText(platformJSON[selectedObject]['Password'
                                  ])

            def saveEditEntry(event):
                import json
                file_path = 'platformAuthentication.json'
                with open(file_path) as f:
                    data = f.read()
                js = json.loads(data)
                js[selectedObject]['Destination Host'] = \
                    destinationHost.getText()
                js[selectedObject]['Username'] = usernameField.getText()
                js[selectedObject]['Password'] = passwordField.getText()
                with open('platformAuthentication.json', 'w') as f:
                    f.write(json.dumps(js))
                refreshDataTable()
                frame.dispose()

            saveEntry = JButton('Ok', actionPerformed=saveEditEntry)

            def cancelEntryFrame(event):
                frame.dispose()

            cancelEntry = JButton('Cancel',
                                  actionPerformed=cancelEntryFrame)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 0
            frame.add(destinationHostJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 0
            frame.add(destinationHost, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 1
            frame.add(authenticationTypeJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 1
            frame.add(authenticationType, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 2
            frame.add(usernameFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 2
            frame.add(usernameField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 3
            frame.add(passwordFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 3
            frame.add(passwordField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridwidth = 1
            gbc.gridx = 1
            gbc.gridy = 4
            frame.add(saveEntry, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridwidth = 1
            gbc.gridx = 2
            gbc.gridy = 4
            frame.add(cancelEntry, gbc)
            frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
            frame.setLocationRelativeTo(None)
            frame.setVisible(True)

        addNewEntrybutton = JButton('Add',
                                    actionPerformed=addCredentials)
        editEntrybutton = JButton('Edit',
                                  actionPerformed=editCredentials)

        def removeNewEntry(event):
            import json
            userSelect = myTable.getSelectedRow()
            file_path = 'platformAuthentication.json'
            with open(file_path) as f:
                entryDeletion = f.read()
            js = json.loads(entryDeletion)
            del js[userSelect]
            with open('platformAuthentication.json', 'w') as f:
                f.write(json.dumps(js))
            refreshDataTable()

        removeEntrybutton = JButton('Remove',
                                    actionPerformed=removeNewEntry)
        head = ['Enabled', 'Destination Host', 'Type', 'Username']

        def fetchCredentials():
            import json
            file_path = 'platformAuthentication.json'
            tableInfo = []
            try:
                fp = open(file_path)
            except IOError:
                fp = open(file_path, 'w+')
                dictionary = [{
                    'Enabled': None,
                    'Destination Host': None,
                    'Type': None,
                    'Username': None,
                    'Password': None,
                    }]
                with open('platformAuthentication.json', 'w') as f:
                    f.write(json.dumps(dictionary))
            platformJSON = json.load(fp)
            with open(file_path) as f:
                platformJSON = json.load(f)
            i = 0
            while i < len(platformJSON):
                newList = []
                newList.append(platformJSON[i]['Enabled'])
                newList.append(platformJSON[i]['Destination Host'])
                newList.append(platformJSON[i]['Type'])
                newList.append(platformJSON[i]['Username'])
                tableInfo.append(newList)
                i = i + 1
            return tableInfo

        data = fetchCredentials()

        def appendNewCredentials(
            Host,
            Type,
            Username,
            Password,
            ):
            import json
            newCredential = {
                'Enabled': True,
                'Destination Host': Host,
                'Type': Type,
                'Username': Username,
                'Password': Password,
                }
            file_path = 'platformAuthentication.json'
            with open(file_path) as f:
                appendData = json.load(f)
            appendData.append(newCredential)
            with open(file_path, 'w') as f:
                json.dump(appendData, f)

        tableModel = TableModel(data, head)
        myTable = JTable()
        panel.setBorder(BorderFactory.createLineBorder(Color(0, 0, 0)))
        jScrollPane.setViewportView(myTable)
        myTable.setModel(tableModel)
        myTable.setAutoCreateRowSorter(True)
        layout = GridBagLayout()
        panel.setLayout(layout)
        gbc = GridBagConstraints()
        gbc.insets = Insets(-765, 0, 0, 5)
        gbc.fill = GridBagConstraints.HORIZONTAL
        gbc.gridx = 0
        gbc.gridy = 1
        panel.add(addNewEntrybutton, gbc)
        gbc.insets = Insets(-705, 0, 0, 5)
        gbc.fill = GridBagConstraints.HORIZONTAL
        gbc.gridx = 0
        gbc.gridy = 2
        panel.add(editEntrybutton, gbc)
        gbc.insets = Insets(-645, 0, 0, 5)
        gbc.fill = GridBagConstraints.HORIZONTAL
        gbc.gridx = 0
        gbc.gridy = 3
        panel.add(removeEntrybutton, gbc)
        gbc.insets = Insets(0, 0, 0, 0)
        gbc.fill = GridBagConstraints.HORIZONTAL
        gbc.gridwidth = 1
        gbc.gridheight = 1
        gbc.gridx = 1
        gbc.gridy = 0
        panel.add(jScrollPane, gbc)
        size = Dimension(900, 400)
        jScrollPane.setPreferredSize(size)

        def refreshDataTable():
            panel.remove(jScrollPane)
            data = fetchCredentials()
            tableModel = TableModel(data, head)
            myTable.setModel(tableModel)
            jScrollPane.setViewportView(myTable)
            panel.add(jScrollPane, gbc)

        return panel

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName('OAuthv1 - Signing')
        callbacks.addSuiteTab(self)

    def processHttpMessage(
        self,
        toolFlag,
        messageIsRequest,
        message,
        ):
        import json
        file_path = 'platformAuthentication.json'
        with open(file_path) as f:
            platformJSON = json.load(f)
        if messageIsRequest:
            for i in platformJSON:
                request = message.getRequest()
                requestInfo = self._helpers.analyzeRequest(request)
                httpRequest = self._helpers.analyzeRequest(message)
                service = message.getHttpService()
                if i['Destination Host'] == service.getHost() and i['Enabled'] == True:
                    consumer_key = i['Username']
                    consumer_key_secret = i['Password']
                    headers = requestInfo.getHeaders()
                    pattern = 'Authorization: OAuth'
                    strHeader = ''
                    for word in headers:
                        strHeader += word

                    inspection = re.search(pattern, strHeader)
                    if inspection != None:
                        pass
                    else:
                        httpMethod = httpRequest.getMethod()
                        httpURL = httpRequest.getUrl()
                        headers.add(prepare_token(httpURL, httpMethod,
                                    consumer_key, consumer_key_secret))
                        body = request[requestInfo.getBodyOffset():]
                        updatedRequest = \
                            self._helpers.buildHttpMessage(headers,
                                body)
                        message.setRequest(updatedRequest)
            else:
                pass

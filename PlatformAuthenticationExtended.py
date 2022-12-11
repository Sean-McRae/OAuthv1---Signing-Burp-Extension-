from burp import IBurpExtender, IHttpListener
from burp import ITab
from javax.swing import JScrollPane, JTable, JPanel, JTextField, JLabel, JComboBox, JButton, table, BorderFactory, JFrame # noqa
from java.awt import Color, GridBagConstraints, GridBagLayout, Insets, Dimension # noqa
from javax.swing.table import DefaultTableModel # noqa
from createSignature import *
from java.lang import String  # noqa
from java.lang import Boolean  # noqa
import re

class TableModel(DefaultTableModel):

    def isCellEditable(self, row, col):
        return col == 0

    def getColumnClass(self, columnIndex):
        if (columnIndex == 0):
            type = Boolean
            return type
        else:
            return String

    def setValueAt( self, value, row, columnIndex ):
        if columnIndex == 0:
            global updateTable
            updateTable(row,value)


class BurpExtender(IBurpExtender, ITab, IHttpListener):

    def getTabCaption(self):
        return 'OAuthv1 - Signing'

    def getUiComponent(self):
        panel = JPanel()
        jScrollPane = JScrollPane()

        global updateTable

        def updateTable(row,value):
            import json
            file_path = 'platformAuthentication.json'
            with open(file_path) as f:
                data = f.read()
            js = json.loads(data)
            js[row]['Enabled'] = value
            with open('platformAuthentication.json', 'w') as f:
                f.write(json.dumps(js))
            refreshDataTable()

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
            Consumer_KeyField = JTextField(30)
            Consumer_KeyFieldJLabel = JLabel('Consumer Key: ')
            Consumer_SecretField = JTextField(30)
            Consumer_SecretFieldJLabel = JLabel('Consumer Secret: ')

            def saveNewEntry(event):
                Host = destinationHost.getText()
                Type = authenticationType.getSelectedItem()
                Consumer_Key = Consumer_KeyField.getText()
                Consumer_Secret = Consumer_SecretField.getText()
                appendNewCredentials(Host, Type, Consumer_Key, Consumer_Secret)
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
            frame.add(Consumer_KeyFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 2
            frame.add(Consumer_KeyField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 3
            frame.add(Consumer_SecretFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 3
            frame.add(Consumer_SecretField, gbc)
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
            Consumer_KeyField = JTextField(30)
            Consumer_KeyFieldJLabel = JLabel('Consumer Key: ')
            Consumer_SecretField = JTextField(30)
            Consumer_SecretFieldJLabel = JLabel('Consumer Secret: ')
            file_path = 'platformAuthentication.json'
            with open(file_path) as f:
                platformJSON = json.load(f)
            selectedObject = myTable.getSelectedRow()
            destinationHost.setText(platformJSON[selectedObject]['Destination Host'
                                    ])
            Consumer_KeyField.setText(platformJSON[selectedObject]['Consumer Key'
                                  ])
            Consumer_SecretField.setText(platformJSON[selectedObject]['Consumer Secret'
                                  ])

            def saveEditEntry(event):
                import json
                file_path = 'platformAuthentication.json'
                with open(file_path) as f:
                    data = f.read()
                js = json.loads(data)
                js[selectedObject]['Destination Host'] = \
                    destinationHost.getText()
                js[selectedObject]['Consumer Key'] = Consumer_KeyField.getText()
                js[selectedObject]['Consumer Secret'] = Consumer_SecretField.getText()
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
            frame.add(Consumer_KeyFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 2
            frame.add(Consumer_KeyField, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 0
            gbc.gridy = 3
            frame.add(Consumer_SecretFieldJLabel, gbc)
            gbc.fill = GridBagConstraints.HORIZONTAL
            gbc.gridx = 1
            gbc.gridy = 3
            frame.add(Consumer_SecretField, gbc)
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
        head = ['Enabled', 'Destination Host', 'Type', 'Consumer Key']

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
                    'Consumer Key': None,
                    'Consumer Secret': None,
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
                newList.append(platformJSON[i]['Consumer Key'])
                tableInfo.append(newList)
                i = i + 1
            return tableInfo

        global data
        data = fetchCredentials()

        def appendNewCredentials(
            Host,
            Type,
            Consumer_Key,
            Consumer_Secret,
            ):
            import json
            newCredential = {
                'Enabled': True,
                'Destination Host': Host,
                'Type': Type,
                'Consumer Key': Consumer_Key,
                'Consumer Secret': Consumer_Secret,
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
                    consumer_key = i['Consumer Key']
                    consumer_key_secret = i['Consumer Secret']
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

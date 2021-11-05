import React from 'react'
import { Admin, Resource } from 'react-admin'
import jsonServerProvider from 'ra-data-json-server'

import { CompanyShow, CompanyList, CompanyCreate } from './components/Companies'
import { UserCreate, UserList } from './components/Users'
import authProvider from './authProvider'

const dataProvider = jsonServerProvider(
  'https://my-json-server.typicode.com/Bandius/myJsonServer'
)

const App: React.FC = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource
      name="companies"
      list={CompanyList}
      show={CompanyShow}
      create={CompanyCreate}
    />
    <Resource
      name="users"
      list={UserList}
      create={UserCreate}
      options={{ label: 'Tenant Admins' }}
    />
  </Admin>
)

export default App

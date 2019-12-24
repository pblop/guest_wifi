import React from 'react'
import './App.css'
import { Form, Input, Button, Icon } from 'antd'
import { Typography } from 'antd'

const { Title, Paragraph } = Typography

class App extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      inputCode: '',
      connected: false,
      incorrectCode: false,
      loading: false
    }
  }

  handleOk = () => {
    this.setState({
      loading: true,
      incorrectCode: false
    })
    fetch('/checkjson', {
      method: 'POST',
      body: JSON.stringify({
        code: this.state.inputCode
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(res => {
        if (res.status === 'connected') {
          this.setState({ loading: false, connected: true })
        } else {
          this.setState({
            loading: false,
            connected: false,
            incorrectCode: true
          })
        }
      })
  }

  render () {
    if (this.state.connected) {
      return (
        <div className='App'>
          <header className='App-header'>
            <Title level={2}>"Ojalá esta Wi-Fi fuera fibra"</Title>
            <Icon type='wifi' style={{ fontSize: '10em', color: '#52c41a' }} />
            <Paragraph style={{ fontSize: '1.5em', color: '#52c41a' }}>
              Estás conectado
            </Paragraph>
          </header>
        </div>
      )
    }
    return (
      <div className='App'>
        <header className='App-header'>
          <Title level={2}>"Ojalá esta Wi-Fi fuera fibra"</Title>
          <Paragraph>
            Introduce el código que está en la pantallita del rúter
          </Paragraph>
          <Form.Item
            validateStatus={this.state.incorrectCode ? 'error' : ''}
            help={this.state.incorrectCode ? 'Código incorrecto' : ''}
          >
            <Input.Group compact size='large' style={{ whiteSpace: 'nowrap' }}>
              <Input
                style={{ width: '6em', textAlign: 'center' }}
                placeholder='Código'
                type='tel'
                maxLength={6}
                onChange={event =>
                  this.setState({
                    inputCode: event.target.value,
                    incorrectCode: false
                  })
                }
                value={this.state.inputCode}
                onPressEnter={this.handleOk}
              />
              <Button
                size='large'
                type='primary'
                icon='wifi'
                loading={this.state.loading}
                onClick={this.handleOk}
              />
            </Input.Group>
          </Form.Item>
        </header>
      </div>
    )
  }
}

export default App

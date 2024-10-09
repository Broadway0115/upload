import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Login = (props) => {
  const [account,setAccount] = useState('')
  const [password, setPassword] = useState('')
//   const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')

  const navigate = useNavigate()

  const onButtonClick = () => {
    // Set initial error values to empty
    // setEmailError('')
    setPasswordError('')
  
    // Check if the user has entered both fields correctly
    // if ('' === account) {
    //   setEmailError('Please enter your username')
    //   return
    // }
  
    // if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    //   setEmailError('Please enter a valid email')
    //   return
    // }
  
    if ('' === password) {
      setPasswordError('Please enter a password')
      return
    }
  
    if (password.length < 7) {
      setPasswordError('The password must be 8 characters or longer')
      return
    }
  
    // Authentication calls will be made here...
    logIn();
  }

  // Call the server API to check if the given email ID already exists
//   const checkAccountExists = (callback) => {
//     fetch('http://localhost:3080/check-account', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ email }),
//     })
//       .then((r) => r.json())
//       .then((r) => {
//         callback(r?.userExists)
//       })
//   }
  
  // Log in a user using email and password
  const logIn = () => {
    console.log({ account, password });
    fetch('https://republique.tw/api-user-auth', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ account, password }),
    })
      .then((r) => r.json())
      .then((r) => {
        console.log(r);
        // if ('success' === r.message) {
        //   localStorage.setItem('user', JSON.stringify({ email, token: r.token }))
        //   props.setLoggedIn(true)
        //   props.setEmail(email)
        //   navigate('/')
        // } else {
        //   window.alert('Wrong email or password')
        // }
      })
  }

  return (
    <div className={'mainContainer'}>
      <div className={'titleContainer'}>
        <div>Login</div>
      </div>
      <br />
      <div className={'inputContainer'}>
        <input
          value={account}
          placeholder="Enter your username here"
          onChange={(ev) => setAccount(ev.target.value)}
          className={'inputBox'}
        />
      </div>
      <br />
      <div className={'inputContainer'}>
        <input
          value={password}
          placeholder="Enter your password here"
          onChange={(ev) => setPassword(ev.target.value)}
          className={'inputBox'}
        />
        <label className="errorLabel">{passwordError}</label>
      </div>
      <br />
      <div className={'inputContainer'}>
        <input className={'inputButton'} type="button" onClick={onButtonClick} value={'Log in'} />
      </div>
    </div>
  )
}

export default Login
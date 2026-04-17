import axios, { InternalAxiosRequestConfig } from 'axios';

import Token from '../types/Token'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Holds the pending request for a new token
let tokenPromise: Promise<string> | null = null;

// Attach authorization header to every request
api.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {

  // Retrieve the JWT from Telegram Secure Storage
  let token = await new Promise<string | null>((resolve) => {
    window.Telegram.WebApp.SecureStorage.getItem('jwt', (err, item) => {
      resolve(err ? null : item);
    });
  });

  // Check if the token is expired
  if (token) {
    try {
      // Extract the payload
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      
      // Decode the Base64 string to JSON
      const payload = JSON.parse(window.atob(base64));

      if (payload.exp < Math.floor(Date.now() / 1000)) {
        token = null;
      }
    } catch (error) {
      token = null
    }
  }

  // Request a new token
  if (!token) {

    // If there are no pending requests for a new token ...
    if (!tokenPromise) {

      // Reach out to the auth endpoint
      tokenPromise = axios.post<Token>(
        import.meta.env.VITE_API_URL + '/auth/token',
        null,
        { headers: { 'X-Telegram-Init-Data': window.Telegram.WebApp.initData } }

      ).then(response => {
        const newToken = response.data.access_token;
        
        // Save the token to the Secure Storage
        window.Telegram.WebApp.SecureStorage.setItem('jwt', newToken)
            
        return newToken;

      }).finally(() => {

        // Indicate that there are no pending requests
        tokenPromise = null;
      });
    }
    
    // Wait until the token arrives
    token = await tokenPromise;
  }

  // Attach the JWT
  config.headers.set('Authorization', `Bearer ${token}`);

  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
const API_CONFIG = {
  development: {
    baseURL: 'http://10.1.4.224:8000',
    timeout: 30000,
  },
  
  production: {
    baseURL: 'https://api.seudominio.com',
    timeout: 30000,
  }
};

const ENV = __DEV__ ? 'development' : 'production';

export const API = {
  baseURL: API_CONFIG[ENV].baseURL,
  timeout: API_CONFIG[ENV].timeout,
  
  endpoints: {
    health: '/health',
    challenge: '/voice/challenge',
    enroll: '/voice/enroll',
    verify: '/voice/verify',
  }
};

export default API;

import axios from 'axios';
import API from './config/api';

const api = axios.create({
  baseURL: API.baseURL,
  timeout: API.timeout,
  headers: {
    'Content-Type': 'application/json',
  }
});
async function getChallengePhrase() {
  try {
    const response = await api.get(API.endpoints.challenge);
    console.log('Frase:', response.data.phrase);
    return response.data.phrase;
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
}

async function enrollUser(userId, phrase, audioUri) {
  try {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('phrase_expected', phrase);
    formData.append('audio_file', {
      uri: audioUri,
      type: 'audio/wav',
      name: 'audio.wav',
    });

    const response = await api.post(API.endpoints.enroll, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('Enrollment:', response.data);
    return response.data;
  } catch (error) {
    console.error('Erro no enrollment:', error);
    throw error;
  }
}

async function verifyUser(userId, phrase, audioUri) {
  try {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('phrase_expected', phrase);
    formData.append('audio_file', {
      uri: audioUri,
      type: 'audio/wav',
      name: 'audio.wav',
    });

    const response = await api.post(API.endpoints.verify, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('Verificação:', response.data);
    return response.data;
  } catch (error) {
    console.error('Erro na verificação:', error);
    throw error;
  }
}

export { api, getChallengePhrase, enrollUser, verifyUser };

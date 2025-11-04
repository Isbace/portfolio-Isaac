// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "Privada",
  authDomain: "khiron-7cf85.firebaseapp.com",
  databaseURL: "https://khiron-7cf85-default-rtdb.firebaseio.com",
  projectId: "khiron-7cf85",
  storageBucket: "khiron-7cf85.appspot.com",
  messagingSenderId: "353230209186",
  appId: "1:353230209186:web:321a08ab67d20ccf5ed7fb",
  measurementId: "G-E1XB07824Q"
};

// Initialize Firebase
const FIREBASE_APP = initializeApp(firebaseConfig);
const FIREBASE_AUTH = getAuth(FIREBASE_APP);

export  {FIREBASE_APP as FIREBASE_APP}; 
export  {FIREBASE_AUTH as FIREBASE_AUTH};


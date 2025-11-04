import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

import { getDatabase, ref, onValue } from "firebase/database";


const db = getDatabase();
const starCountRef = ref(db, 'posts/' + postId + '/starCount');
onValue(starCountRef, (snapshot) => {
  const data = snapshot.val();
  console.log(data);
});
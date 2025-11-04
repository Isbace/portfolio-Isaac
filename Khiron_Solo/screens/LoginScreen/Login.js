import { View, Text, StyleSheet, TextInput, Button, ActivityIndicator } from 'react-native';
import React, { useState } from 'react';
import { FIREBASE_APP } from '../../FirebaseConfig';
import { FIREBASE_AUTH } from '../../FirebaseConfig';
import { getDatabase } from 'firebase/database';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
//import SignUp from '../SignUpScreen/SignUpScreen';
//import { useNavigation } from 'expo-router';


const database = getDatabase(FIREBASE_APP);

const Login = ({ navigation }) => {
    //const navigation = useNavigation();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState('');
    const auth = FIREBASE_AUTH

    const LogIn = async () =>{
        setLoading(true);
        try{
            const response = await signInWithEmailAndPassword(auth, email, password);
        } catch (error){
            console.log(error);
            alert('Sign in  failed: ' + error.message);
        } finally {
            setLoading(false);
        }
    }


    return (
        <View style={styles.container}>
            <TextInput value={email} style = {styles.input} placeholder='Email' autoCapitalize='none' onChangeText={(text) => setEmail(text)}></TextInput>
            <TextInput secureTextEntry={true} value={password} style = {styles.input} placeholder='Password' autoCapitalize='none' onChangeText={(text) => setPassword(text)}></TextInput>
            
            {loading ? (
            <ActivityIndicator size="large" color = "#0000ff" />
            ) : (
                <>
                    <Button title="Login" onPress = {LogIn}/>
                    <Button title="Create Account" onPress={() => navigation.navigate('Sign Up Screen')} />
                </>
            )}
        </View>
    )
};

export default Login;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
    input:{
        marginVertical: 4,
        height: 50,
        borderWidth: 1,
        borderRadius: 4,
        padding: 10,
        backgroundColor: '#fff'
    }
  });
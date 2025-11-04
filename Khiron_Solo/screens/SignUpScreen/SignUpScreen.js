import { View, Text, StyleSheet, TextInput, Button, ActivityIndicator } from 'react-native';
import React, { useState } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { FIREBASE_AUTH } from '../../FirebaseConfig';
import { FIREBASE_APP } from '../../FirebaseConfig';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { getDatabase, ref, set, push, onValue } from "firebase/database";
//import Login from '../LoginScreen/Login';

const db = getDatabase(FIREBASE_APP);

const Stack = createNativeStackNavigator();

const SignUpScreen = ({ navigation }) => {
    //const navigation = useNavigation();
    const [userId, setUserId] = useState('');
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState('');
    const auth = FIREBASE_AUTH

    const userData = {
        Email: email,
        Name: name
    }

    const signUp = async () =>{
        setLoading(true);
        const usersRef = ref(db, 'Users/-NtY75dPoMyCVXPD2ISa');
        try{
            const response = await createUserWithEmailAndPassword(auth, email, password);
            const newUser = response.user; // Get the user object from UserCredential
            set(ref(db, 'Users/' + newUser.uid), userData);

            //Don't delete this part. It makes it work for some reason
            onValue(usersRef, (snapshot) => {
            const data = snapshot.val();
            console.log(data.Email);
            });
            
        } catch (error){
            console.log(error);
            alert('Sign in  failed: ' + error.message);
        } finally {
            setLoading(false);

        }
    }

    return (
        <View style={styles.container}>
            <TextInput value={name} style = {styles.input} placeholder='Name' autoCapitalize='none' onChangeText={(text) => setName(text)}></TextInput>
            <TextInput value={email} style = {styles.input} placeholder='Email' autoCapitalize='none' onChangeText={(text) => setEmail(text)}></TextInput>
            <TextInput secureTextEntry={true} value={password} style = {styles.input} placeholder='Password' autoCapitalize='none' onChangeText={(text) => setPassword(text)}></TextInput>
            
            {loading ? (
            <ActivityIndicator size="large" color = "#0000ff" />
            ) : (
                <>
                    <Button title="Create Account" onPress={signUp} />
                    <Button title="Login" onPress = {() => navigation.navigate('Log In Screen')}/>
                </>
            )}
        </View>
    )
};

export default SignUpScreen;

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
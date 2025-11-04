import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { User, onAuthStateChanged } from 'firebase/auth'
import {useState, useEffect} from 'react'
import ProfileScreen from './screens/ProfileScreen/ProfileScreen';
import LoginScreen from './screens/LoginScreen/Login';
import SettingScreen from './screens/SettingScreen/SettingScreen';
import SignUpScreen from './screens/SignUpScreen/SignUpScreen';
import { getDatabase, ref, get, child, onValue } from "firebase/database";
import HomeScreen from './screens/HomeScreen/HomeScreen';
import ActivityLogScreen from './screens/ActivityLogScreen/ActivityLogScreen';
import LoadingScreen from './screens/LoadingScreen/LoadingScreen';
import { FIREBASE_AUTH } from './FirebaseConfig';
import { FIREBASE_APP } from './FirebaseConfig';


const db = getDatabase(FIREBASE_APP);

const Stack = createNativeStackNavigator();

const InsideStack = createNativeStackNavigator();

const LogInStack = createNativeStackNavigator();



function InsideLayout(){
  return (
    <InsideStack.Navigator>
      <InsideStack.Screen name = "Home Screen" component = {HomeScreen} options={{headerShown: false}}/>
    </InsideStack.Navigator>
  )
}

function LoginLayout(){
  return (
    <LogInStack.Navigator>
      <LogInStack.Screen name = "Log In Screen" component = {LoginScreen} options={{headerShown: false}}/>
      <LogInStack.Screen name = "Sign Up Screen" component = {SignUpScreen} options={{headerShown: false}}/>
    </LogInStack.Navigator>
  )
}

export default function App() {
  const [userData, setUserData] = useState();
  const [userId, setUserId] = useState('');
  const [user, setUser] = useState(null);
  const [loadingScreen, setLoadingScreen] = useState(false);

  useEffect (() => {
    const unsubscribe = onAuthStateChanged(FIREBASE_AUTH, (user) => {
      setUser(user);
      console.log(user.email);
      setLoadingScreen(true);
      setUserId(user.uid);
    });

    if (loadingScreen) {
      setTimeout(() => {
        setLoadingScreen(false);
      }, 3000);
      return <LoadingScreen />;
    }

    return unsubscribe;
  }, []);

  useEffect(() => {
    if (userId){
      //console.log(userId);
      const dbRef = ref(db);
      const usersRef = ref(db, 'Users/' + userId);
  
      get(child(dbRef, 'Users/' + userId)).then((snapshot) => {
        if (snapshot.exists()) {
          setUserData(snapshot.val());
          
        } else {
          console.log("No data available");
        }
      }).catch((error) => {
        console.error(error);
      });
      // onValue(usersRef, (snapshot) => {
      //   setUserData(snapshot.val());
      //   console.log(userData.Email);
      // });
      //console.log(userData);
    } 
  }, [userId]);
  
  //component={ProfileScreen}

  return (
    
    <NavigationContainer>
      <Stack.Navigator initialRouteName = 'Login'>
        {user ? (
          <Stack.Screen name='Inside' component={InsideLayout} options={{headerShown: false}}/>
        ) : (
          <Stack.Screen name='Login' component={LoginLayout} options={{headerShown: false}}/>
        )}
        <Stack.Screen name="ProfileScreen"  options={{ headerShown: false }} >
          {(props) => <ProfileScreen {...props} userData={userData} userId ={userId}/>}
        </Stack.Screen>
        <Stack.Screen name="ActivityLogScreen" component={ActivityLogScreen} options={{ headerShown: false, animation: 'slide_from_left' }} />
        <Stack.Screen name="SettingScreen" component={SettingScreen}/>
      </Stack.Navigator>
    </NavigationContainer>

  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});


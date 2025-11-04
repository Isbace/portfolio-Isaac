import { View, Text, StyleSheet, Button } from "react-native";
import { Image, StatusBar } from "react-native";
import { useFonts } from 'expo-font';

export default function LoadingScreen(){
    const logo = require('../../assets/Logo-03.png');
    //const GothamFont = require('../../assets/fonts/Gotham_Regular/Gotham_Regular.otf')
    //const [fontsLoaded] = useFonts(GothamFont)
    return(
        <View style={styles.container}>
            <Text style={styles.mainTitle}>SOLO</Text>
            <StatusBar style="auto" />
            <Text style={styles.PoweredBy}>Powered By</Text>
            <Image source={logo} style={styles.KhironLogo}  />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#0ABC71',
      color: '#fff',
      width: '100%',
      alignItems: 'center',
      justifyContent: 'center',
    },
    mainTitle: {
        marginTop: 225,
        color: '#fff',
        fontSize: 64, 
        fontWeight: 'bold',
        //fontFamily: 'Gotham'
    },
    PoweredBy: {
        fontSize: 24, 
        marginTop: 200,
        marginBottom: -180,
        color: '#fff',
        //fontFamily: 'Gotham'
    },
    KhironLogo:{
        width: 200,
        height: 100,
        marginTop: 150
    }
  });
import React, {useState} from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, SafeAreaView} from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { Feather } from '@expo/vector-icons';
import ImagePicker from 'react-native-image-picker';
import ProfileImage from '../../assets/pfp.jpg';

export default function ProfileScreen({navigation, userData}) {

  return (
    <View style={styles.container}>
        <Text>Hello World</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F2',
    padding: 20,
  }
});

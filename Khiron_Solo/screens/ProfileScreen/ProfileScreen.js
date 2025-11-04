import React, {useEffect, useState} from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Modal, TextInput, Button} from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { Octicons } from '@expo/vector-icons';
import { Entypo } from '@expo/vector-icons';
import { Feather } from '@expo/vector-icons';
import ImagePicker from 'react-native-image-picker';
import { getDatabase, ref, set, get, child, push, onValue } from "firebase/database";
import ProfileImage from '../../assets/pfp.jpg';
import { FIREBASE_APP } from '../../FirebaseConfig';

export default function ProfileScreen({navigation, userId}) {
  const db = getDatabase(FIREBASE_APP);
  const formatPhoneNumber = (phoneNumber) => {
    // Assuming phoneNumber format is '1234567890'
    phoneNumber = String(phoneNumber);
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6)}`;
  };
  const [profilePic, setProfilePic] = useState(ProfileImage);
  const [modalVisible, setModalVisible] = useState(false);
  const [newContactName, setNewContactName] = useState('');
  const [newContactNumber, setNewContactNumber] = useState('');
  const [userData, setUserData] = useState();

  useEffect(() => {
     //console.log(userId);
     const dbRef = ref(db);
     //const usersRef = ref(db, 'Users/' + userId);
 
     get(child(dbRef, 'Users/' + userId)).then((snapshot) => {
       if (snapshot.exists()) {
         setUserData(snapshot.val());
         
       } else {
         console.log("No data available");
       }
     }).catch((error) => {
       console.error(error);
     });
  }, [userId]);
  
  
  //console.log(userDat);
  

  const selectImage = () => {
    const options = {
      title: 'Select Profile Picture',
      cancelButtonTitle: 'Cancel',
      takePhotoButtonTitle: 'Take Photo',
      chooseFromLibraryButtonTitle: 'Choose from Library',
      quality: 0.5,
      maxWidth: 500,
      maxHeight: 500,
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };

    ImagePicker.showImagePicker(options, response => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else {
        const source = { uri: response.uri };
        setProfilePic(source);
      }
    });
  };

  const saveNewContact = () => {
    const contactIds = userData ? Object.keys(userData.Contacts) :[];
    set(ref(db, 'Users/' + userId+'/Contacts/Contact'+(contactIds.length + 1).toString()), {
      Name: newContactName,
      Number: newContactNumber
    });
    setModalVisible(false);
    // Clear input fields
    setNewContactName('');
    setNewContactNumber('');
  };

  return (
    <View style={styles.container}>
      {userData && (
      <><TouchableOpacity onPress={() => navigation.navigate('SettingScreen')}>
          <AntDesign style={styles.settingsIcon} name="setting" size={24} color="black" />
        </TouchableOpacity><View style={styles.profileContainer} onPress={selectImage}>
            <View style={styles.profileContainer}>
              <View style={styles.imageContainer}>
                <Image
                  style={styles.profileImage}
                  source={profilePic} />
              </View>
              <TouchableOpacity style={styles.editIconContainer} onPress={selectImage}>
                <Octicons name="pencil" size={24} color="black" />
              </TouchableOpacity>
              <Text style={styles.profileName}>{userData.Name}</Text>
              <Text style={styles.profileEmaiL}>{userData.Email}</Text>
            </View>
          </View><View style={styles.emergencyContainer}>
            <Text style={styles.emergencyTitle}>Emergency Contacts</Text>
            {userData && userData.Contacts && Object.keys(userData.Contacts).map((contactId, index) => (
              <TouchableOpacity key={index} style={styles.contactContainer}>
                <Text style={styles.contactName}>{userData.Contacts[contactId].Name}</Text>
                <Text style={styles.contactNumber}>{formatPhoneNumber(userData.Contacts[contactId].Number)}</Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity style={styles.addButton} onPress={() => setModalVisible(true)}>
              <Text style={styles.addButtonText}>Add Contact</Text>
            </TouchableOpacity>
            <Modal
              animationType="slide"
              transparent={true}
              visible={modalVisible}
              onRequestClose={() => setModalVisible(false)}
            >
              <View style={styles.modalContainer}>
                <View style={styles.modalContent}>
                  <Text style={styles.modalTitle}>Add New Contact</Text>
                  <TextInput
                    style={styles.input}
                    placeholder="Name"
                    onChangeText={text => setNewContactName(text)}
                    value={newContactName} />
                  <TextInput
                    style={styles.input}
                    placeholder="Phone Number"
                    keyboardType="phone-pad"
                    onChangeText={text => setNewContactNumber(text)}
                    value={newContactNumber} />
                  <View style={styles.modalButtons}>
                    <TouchableOpacity style={styles.modalButton} onPress={() => setModalVisible(false)}>
                      <Text style={styles.modalButtonText}>Cancel</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.modalButton} onPress={saveNewContact}>
                      <Text style={styles.modalButtonText}>Confirm</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              </View>
            </Modal>
          </View></>
      )}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.navButton}>
          <Feather name="activity" size={40} color="white" onPress={() => navigation.navigate('ActivityLogScreen')}/>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton}>
          <Feather name="home" size={40} color="white" onPress={() => navigation.navigate('Inside')} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('ProfileScreen')}>
          <AntDesign name="user" size={40} color="white" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F2',
    padding: 20,
  },
  profileContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  profileEmail:{
    fontSize: 16,
    fontWeight: 'bold'
  },
  imageContainer:{
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.45,
    shadowRadius: 3.84,
    marginBottom: 15
  },
  profileImage: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 10,
    marginTop: 50,
  },
  profileName: {
    fontSize: 30,
    fontWeight: 'bold',
  },
  emergencyContainer: {
    borderTopWidth: 1,
    borderTopColor: '#CCCCCC',
    paddingTop: 20,
  },
  emergencyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  contactContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 10,
    marginBottom: 10,
  },
  contactName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  contactNumber: {
    fontSize: 14,
  },
  navButton: {
    backgroundColor: '#383838',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    backgroundColor: '#383838',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    paddingVertical: 30,
  },
  settingsIcon: {
    marginTop: 30,
    fontSize: 30,
    left: 320
  },
  editIconContainer: {
    position: 'absolute',
    bottom: 75,
    right: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.45,
    shadowRadius: 3.84,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 20,
    width: '80%',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#CCCCCC',
    borderRadius: 5,
    marginBottom: 10,
    paddingHorizontal: 10,
    height: 50
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 10
  },
  modalButton: {
    marginLeft: 10,
  },
  modalButtonText: {
    color: '#007BFF',
    fontSize: 16,
  },
});

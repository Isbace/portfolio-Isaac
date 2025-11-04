import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { Feather } from '@expo/vector-icons';

export default function HomePage({navigation}) {
  const [timer, setTimer] = useState(0);
  const [timerRunning, setTimerRunning] = useState(false);
  const intervalRef = useRef(null);

  const startTimer = () => {
    setTimerRunning(true);
    intervalRef.current = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);
  };

  const stopTimer = () => {
    setTimerRunning(false);
    clearInterval(intervalRef.current);
  };

  const resetTimer = () => {
    setTimer(0);
    clearInterval(intervalRef.current);
    setTimerRunning(false);
  };

  const saveTimer = () => {
    // Here you can implement the logic to save timer information
    // For example, you can save it to AsyncStorage or send it to a server
    // This is just a placeholder function
    console.log("Timer information saved:", timer);
  };

  const formatTime = (timeInSeconds) => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = timeInSeconds % 60;
    return `${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
  };

  const buttonColor = timerRunning ? 'red' : '#0ABC71';

  return (
    <View style={styles.container}>
      <View style={[styles.section, styles.section1]}>
        <Text style={styles.soloText}>SOLO</Text>
      </View>
      <View style={[styles.section, styles.section2]}>
        <View style={styles.timerBox}>
          <Text style={styles.timerText}>{formatTime(timer)}</Text>
        </View>
        <View style={styles.buttonsContainer}>
          <TouchableOpacity style={[styles.button, { backgroundColor: buttonColor }]} onPress={timerRunning ? stopTimer : startTimer}>
            <Text style={styles.buttonText}>
              {timerRunning ? 'Stop Activity' : 'Start Activity'}
            </Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.resetButton]} onPress={resetTimer}>
            <Text style={styles.buttonText}>Reset Timer</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.saveButton]}  onPress={() => {
                  resetTimer();
                  navigation.navigate('ActivityLogScreen', { timer: timer });
                }}>
            <Text style={styles.buttonText}>Save Activity</Text>
            
          </TouchableOpacity>
        </View>
      </View>
      <View style={[styles.section, styles.section3]}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.navButton}  onPress={() => navigation.navigate('ActivityLogScreen')}>
            <Text style={styles.buttonText}>
              <Feather name="activity" size={40} color="white" />
            </Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Inside')}>
            <Feather name="home" size={40} color="white" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('ProfileScreen')}>
            <AntDesign name="user" size={40} color="white" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F2',
    width: '100%',
  },
  section: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  section1: {
    marginBottom: 10,
    alignItems: 'left',
    color: '#0ABC71',
  },
  section2: {
    marginVertical: 10,
  },
  section3: {
    marginTop: 300,
    paddingTop: 40,
    height: 50,
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    backgroundColor: '#f2f2f2',
  },
  soloText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#0ABC71',
    paddingLeft: 20,
  },
  timerBox: {
    width: 325,
    height: 150,
    backgroundColor: '#ffffff',
    marginTop: 250,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  timerText: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  buttonsContainer: {
    alignItems: 'center',
  },
  button: {
    marginTop: 20,
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
  },
  resetButton: {
    backgroundColor: '#606A69',
    marginTop: 10,
  },
  saveButton: {
    backgroundColor: '#4287f5', // Change color according to your design
    marginTop: 10,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  navButton: {
    marginTop: 20,
    backgroundColor: '#383838',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  buttonContainer: {
    backgroundColor: '#383838',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    marginTop: 35,
    paddingBottom: 40,
    paddingTop: 10,
  },
});

import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <View style={styles.loadviewTop}>
          <Text>loading view top</Text>
        </View>
        <View style={styles.loadviewButtom}>
          <Text>loading view buttom</Text>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  loadviewTop: {
    flex: 1,
    backgroundColor : '#4682B4',
    alignItems: 'center',
  },
  loadviewButtom:{
    flex: 1,
    backgroundColor: '#F0F0F0',
    alignItems : 'center',
  },
});

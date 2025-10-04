import React, { useEffect, useState } from 'react';
import {
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    View,
    ActivityIndicator,
    Button,
    useColorScheme,
} from 'react-native';
import { apiService } from './src/services/api';

function App(): React.JSX.Element {
    const isDarkMode = useColorScheme() === 'dark';
    const [healthStatus, setHealthStatus] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    const backgroundStyle = {
        backgroundColor: isDarkMode ? '#1a1a1a' : '#f5f5f5',
    };

    const checkHealth = async () => {
        setLoading(true);
        setError('');
        setHealthStatus('');

        try {
            const response = await apiService.healthCheck();
            if (response.error) {
                setError(response.error);
            } else if (response.data) {
                setHealthStatus(JSON.stringify(response.data, null, 2));
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkHealth();
    }, []);

    return (
        <SafeAreaView style={[styles.container, backgroundStyle]}>
            <StatusBar
                barStyle={isDarkMode ? 'light-content' : 'dark-content'}
                backgroundColor={backgroundStyle.backgroundColor}
            />
            <ScrollView
                contentInsetAdjustmentBehavior="automatic"
                style={backgroundStyle}>
                <View style={styles.content}>
                    <Text style={[styles.title, { color: isDarkMode ? '#fff' : '#000' }]}>
                        HackYeah 2025
                    </Text>
                    <Text
                        style={[styles.subtitle, { color: isDarkMode ? '#ccc' : '#666' }]}>
                        React Native + FastAPI
                    </Text>

                    <View style={styles.card}>
                        <Text
                            style={[
                                styles.cardTitle,
                                { color: isDarkMode ? '#fff' : '#000' },
                            ]}>
                            Backend Health Check
                        </Text>

                        {loading && (
                            <ActivityIndicator size="large" color="#007AFF" style={styles.loader} />
                        )}

                        {error && (
                            <View style={styles.errorContainer}>
                                <Text style={styles.errorText}>❌ Error: {error}</Text>
                                <Text style={styles.helpText}>
                                    Make sure the backend is running at the configured API_BASE_URL
                                </Text>
                            </View>
                        )}

                        {healthStatus && (
                            <View style={styles.successContainer}>
                                <Text style={styles.successText}>✅ Connected!</Text>
                                <Text
                                    style={[
                                        styles.responseText,
                                        { color: isDarkMode ? '#ccc' : '#333' },
                                    ]}>
                                    {healthStatus}
                                </Text>
                            </View>
                        )}

                        <Button title="Retry" onPress={checkHealth} disabled={loading} />
                    </View>

                    <View style={styles.infoCard}>
                        <Text
                            style={[
                                styles.infoTitle,
                                { color: isDarkMode ? '#fff' : '#000' },
                            ]}>
                            Quick Start
                        </Text>
                        <Text
                            style={[
                                styles.infoText,
                                { color: isDarkMode ? '#ccc' : '#666' },
                            ]}>
                            1. Make sure the FastAPI backend is running{'\n'}
                            2. Check your .env file for correct API_BASE_URL{'\n'}
                            3. For Android emulator: use http://10.0.2.2:8000{'\n'}
                            4. For physical device: use your local IP
                        </Text>
                    </View>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    content: {
        padding: 20,
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        textAlign: 'center',
        marginTop: 20,
        marginBottom: 8,
    },
    subtitle: {
        fontSize: 16,
        textAlign: 'center',
        marginBottom: 30,
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 20,
        marginBottom: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    cardTitle: {
        fontSize: 20,
        fontWeight: '600',
        marginBottom: 15,
    },
    loader: {
        marginVertical: 20,
    },
    errorContainer: {
        backgroundColor: '#ffebee',
        borderRadius: 8,
        padding: 15,
        marginBottom: 15,
    },
    errorText: {
        color: '#c62828',
        fontSize: 14,
        fontWeight: '500',
        marginBottom: 8,
    },
    helpText: {
        color: '#d32f2f',
        fontSize: 12,
    },
    successContainer: {
        backgroundColor: '#e8f5e9',
        borderRadius: 8,
        padding: 15,
        marginBottom: 15,
    },
    successText: {
        color: '#2e7d32',
        fontSize: 16,
        fontWeight: '600',
        marginBottom: 8,
    },
    responseText: {
        fontFamily: 'monospace',
        fontSize: 12,
    },
    infoCard: {
        backgroundColor: '#e3f2fd',
        borderRadius: 12,
        padding: 20,
        marginBottom: 20,
    },
    infoTitle: {
        fontSize: 18,
        fontWeight: '600',
        marginBottom: 12,
    },
    infoText: {
        fontSize: 14,
        lineHeight: 22,
    },
});

export default App;

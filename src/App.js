import React, { useState } from 'react';
import ThemeToggle from './ThemeToggle';

const dummyData = {
  aggregate_metrics: {
    total_lines: 1200,
    total_files: 15,
    functions: 45,
    classes: 10,
    structs: 5,
    loops: 25,
    conditionals: 60,
    cyclomatic_complexity: 85,
  },
  file_metrics: [
    {
      file: 'src/main.cpp',
      lines: 300,
      functions: 10,
      complexity: 'High',
    },
    {
      file: 'src/utils.cpp',
      lines: 150,
      functions: 5,
      complexity: 'Medium',
    },
    {
      file: 'src/helpers.h',
      lines: 50,
      functions: 2,
      complexity: 'Low',
    },
  ],
  ai_music_theme: {
    mood: 'Mysterious',
    tempo: 92,
    scale: 'D minor',
    instruments: ['violin', 'low piano', 'shaker'],
    tags: ['suspense', 'tension'],
  },
  music_path: 'output/result.wav',
};

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      // Simulate API call
      setTimeout(() => {
        setData(dummyData);
        setLoading(false);
      }, 2000);
    }
  };

  const handleRegenerate = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setData({
        ...dummyData,
        ai_music_theme: {
          ...dummyData.ai_music_theme,
          mood: 'Chaotic',
          tempo: 150,
          scale: 'C# minor',
        },
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <div className="container mx-auto p-4">
        <h1 className="text-4xl font-bold text-center mb-8">Code to Music</h1>
        <div className="flex justify-center mb-8">
          <input type="file" accept=".zip" onChange={handleFileUpload} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"/>
        </div>
        {loading && <div className="text-center">Loading...</div>}
        {data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-1">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">🎧 {data.ai_music_theme.mood}</h2>
                <p className="mb-2">🎼 {data.ai_music_theme.tempo} BPM, {data.ai_music_theme.scale}</p>
                <p className="mb-4">Instruments: {data.ai_music_theme.instruments.join(', ')}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {data.ai_music_theme.tags.map((tag) => (
                    <span key={tag} className="bg-blue-100 text-blue-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800">{tag}</span>
                  ))}
                </div>
                <audio controls src={data.music_path} className="w-full mb-4"></audio>
                <button onClick={handleRegenerate} className="w-full bg-violet-500 text-white py-2 rounded-lg hover:bg-violet-600">Regenerate Music</button>
              </div>
            </div>
            <div className="md:col-span-2">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">File Metrics</h2>
                <ul>
                  {data.file_metrics.map((file) => (
                    <li key={file.file} className="border-b border-gray-200 dark:border-gray-700 py-2">
                      <div className="flex justify-between">
                        <span>{file.file}</span>
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          file.complexity === 'High' ? 'bg-red-100 text-red-800' :
                          file.complexity === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {file.complexity}
                        </span>
                      </div>
                      <div className="text-sm text-gray-500">
                        Lines: {file.lines}, Functions: {file.functions}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

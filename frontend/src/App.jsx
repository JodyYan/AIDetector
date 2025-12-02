import React, { useState } from 'react';
// 新增引入 Trash2 (垃圾桶圖示)
import { Clipboard, FileText, Upload, AlertCircle, CheckCircle, Loader2, Trash2 } from 'lucide-react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleTextChange = (e) => {
    setText(e.target.value);
    if (result) setResult(null);
  };

  // --- 新增：清空功能 ---
  const handleClear = () => {
    setText('');       // 清空文字
    setResult(null);   // 清空結果
  };

  const handlePaste = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      setText(clipboardText);
      setResult(null);
    } catch (err) {
      alert("無法讀取剪貼簿，請手動貼上。");
    }
  };

  const handleSample = () => {
    const sample = "Deep learning models have demonstrated remarkable capabilities in natural language processing tasks. However, distinguishing between human-written and machine-generated text remains a significant challenge in the current digital landscape.";
    setText(sample);
    setResult(null);
  };

  const handleCheck = async () => {
    if (!text.trim()) return;
    
    setIsLoading(true);
    setResult(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/detect', {
        text: text
      });
      setResult(response.data);
    } catch (error) {
      console.error("API Error:", error);
      alert("無法連接伺服器，請確認後端視窗是否開啟。");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center py-12 px-4 font-sans text-gray-800">
      
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-slate-900 mb-3 tracking-tight">
          AI Detector by JustDone
        </h1>
        <p className="text-lg text-gray-500">
          Maintain the authenticity of your writing by identifying AI-generated content.
        </p>
      </div>

      <div className="w-full max-w-4xl bg-[#F4F6F8] rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative" style={{ minHeight: '450px' }}>
        
        {/* 文字輸入框 */}
        <textarea
          className="w-full flex-grow bg-transparent p-8 text-lg text-gray-700 placeholder-gray-400 focus:outline-none resize-none"
          placeholder="Enter text here or upload file to check for AI Content."
          value={text}
          onChange={handleTextChange}
        />

        {/* --- 新增：清空按鈕 (右上角) --- */}
        {/* 只有當有文字時才顯示此按鈕 */}
        {text && (
          <button
            onClick={handleClear}
            className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 hover:bg-white rounded-full shadow-sm transition-all duration-200"
            title="Clear content"
          >
            <Trash2 size={20} />
          </button>
        )}

        {/* 中間的操作按鈕 (當沒有文字時顯示) */}
        {!text && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="flex gap-4 pointer-events-auto">
              <ActionButton icon={<Clipboard size={24} />} label="Paste Text" onClick={handlePaste} />
              <ActionButton icon={<FileText size={24} />} label="Sample Text" onClick={handleSample} />
              <ActionButton icon={<Upload size={24} />} label="Upload File" onClick={() => alert("File upload feature coming soon!")} />
            </div>
          </div>
        )}

        <div className="bg-white p-4 flex justify-between items-center border-t border-gray-100">
          
          <div className="pl-2">
            {result && (
              <div className={`flex items-center gap-2 text-lg font-bold ${result.is_ai ? 'text-red-500' : 'text-green-600'}`}>
                {result.is_ai ? <AlertCircle size={24}/> : <CheckCircle size={24}/>}
                <span>{result.message} ({result.score}%)</span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400 font-medium">
              {text.length} chars
            </span>
            <button
              onClick={handleCheck}
              disabled={!text.trim() || isLoading}
              className={`px-8 py-3 rounded-full font-bold text-white transition-all duration-200 flex items-center gap-2
                ${!text.trim() || isLoading 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-slate-800 hover:bg-slate-900 hover:shadow-lg'}`}
            >
              {isLoading && <Loader2 className="animate-spin" size={20} />}
              {isLoading ? 'Checking...' : 'Check for AI Content'}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

const ActionButton = ({ icon, label, onClick }) => (
  <button 
    onClick={onClick}
    className="flex flex-col items-center justify-center bg-white w-36 h-28 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md hover:-translate-y-1 transition-all duration-200 group"
  >
    <div className="text-gray-400 group-hover:text-slate-700 mb-3">{icon}</div>
    <span className="text-sm font-semibold text-gray-500 group-hover:text-slate-700">{label}</span>
  </button>
);

export default App;
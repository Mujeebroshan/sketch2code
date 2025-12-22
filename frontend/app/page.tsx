"use client";

import { useState, useRef, useEffect } from "react";
import { Upload, Sparkles, AlertCircle, Copy, Check, Code, Eye, Download, Send, Zap, Monitor, Smartphone, Moon } from "lucide-react";
import PreviewFrame from "../components/PreviewFrame";
import Editor from "@monaco-editor/react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("Initializing..."); // New for Smart Loader
  const [isRefining, setIsRefining] = useState(false);
  const [generatedCode, setGeneratedCode] = useState<string>("");
  const [instruction, setInstruction] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview");

  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // URL CONFIG
  const BACKEND_URL = "https://sketch2code-xi55.onrender.com";

  // --- SMART LOADING LOGIC ---
  useEffect(() => {
    if (isLoading) {
      const steps = [
        "Uploading sketch...",
        "Gemini 3 is analyzing the design...",
        "Detecting layout structure...",
        "Writing Tailwind CSS...",
        "Polishing interactions..."
      ];
      let i = 0;
      setLoadingStep(steps[0]);
      const interval = setInterval(() => {
        i = (i + 1) % steps.length;
        setLoadingStep(steps[i]);
      }, 1500); // Change text every 1.5 seconds
      return () => clearInterval(interval);
    }
  }, [isLoading]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const generateCode = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setError(null);
    setActiveTab("preview");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${BACKEND_URL}/generate`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Generation failed");
      const data = await response.json();
      setGeneratedCode(data.html);
    } catch (err) {
      setError("Server error. Check backend terminal.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefine = async () => {
    if (!generatedCode || !instruction.trim()) return;
    setIsRefining(true);
    
    const formData = new FormData();
    formData.append("code", generatedCode);
    formData.append("instruction", instruction);

    try {
      const response = await fetch(`${BACKEND_URL}/refine`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Refinement failed");
      const data = await response.json();
      setGeneratedCode(data.html); 
      setInstruction(""); 
    } catch (err) {
      setError("Failed to update code. Try again.");
    } finally {
      setIsRefining(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCode = () => {
    const blob = new Blob([generatedCode], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "index.html";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-[#0F1117] text-white flex flex-col font-sans selection:bg-indigo-500/30 overflow-hidden relative">
      
      {/* Background Grid Pattern */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none"></div>

      {/* Header */}
      <header className="border-b border-white/5 bg-gray-900/40 backdrop-blur-xl sticky top-0 z-20">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 border border-white/10">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Sketch2Code
              </h1>
              <p className="text-[10px] text-gray-500 font-mono tracking-widest uppercase">PRO EDITION</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
             <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-white/5 rounded-full border border-white/10">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"/>
                <span className="text-xs text-gray-300 font-medium">Gemini 3 Online</span>
             </div>
          </div>
        </div>
      </header>

      <div className="flex-1 flex flex-col md:flex-row h-[calc(100vh-73px)] relative z-10">
        
        {/* LEFT COLUMN: Controls */}
        <div className="w-full md:w-[420px] flex flex-col border-b md:border-r border-white/5 bg-gray-900/60 backdrop-blur-sm">
          <div className="flex-1 p-6 flex flex-col space-y-6 overflow-y-auto custom-scrollbar">
            
            {/* Upload Zone */}
            <div 
              onClick={() => fileInputRef.current?.click()}
              className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer group overflow-hidden ${selectedFile ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-white/10 hover:border-indigo-500/50 hover:bg-white/5'}`}
            >
              <input type="file" ref={fileInputRef} onChange={handleFileSelect} className="hidden" accept="image/*" />
              
              <div className="flex flex-col items-center gap-4 relative z-10">
                {previewUrl ? (
                  <div className="relative w-full group-hover:scale-[1.02] transition-transform duration-300">
                    <img src={previewUrl} alt="Preview" className="w-full rounded-xl shadow-2xl ring-1 ring-white/10" />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-xl backdrop-blur-sm">
                      <p className="text-white font-medium flex items-center gap-2"><Upload size={18}/> Change Image</p>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors border border-white/10">
                      <Upload className="w-8 h-8 text-gray-400 group-hover:text-indigo-400" />
                    </div>
                    <div>
                      <p className="text-gray-200 font-medium">Drop your sketch here</p>
                      <p className="text-gray-500 text-sm mt-1">or click to browse</p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Main Action Button */}
            <button
              onClick={generateCode}
              disabled={isLoading || !selectedFile}
              className={`w-full font-bold py-4 px-6 rounded-xl transition-all duration-300 shadow-xl flex items-center justify-center gap-3 relative overflow-hidden group ${
                isLoading 
                ? 'bg-gray-800 cursor-not-allowed opacity-50' 
                : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white hover:shadow-indigo-500/25 ring-1 ring-white/20'
              }`}
            >
              {isLoading ? (
                <span className="text-gray-300">Processing...</span>
              ) : (
                <>
                  <span className="relative z-10 flex items-center gap-2">
                    <Sparkles size={20} className={previewUrl ? "animate-pulse" : ""} /> 
                    Generate Code
                  </span>
                  <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"/>
                </>
              )}
            </button>
            
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm flex gap-3 items-start">
                <AlertCircle className="w-5 h-5 shrink-0" />
                <p>{error}</p>
              </div>
            )}
          </div>

          {/* Chat Interface */}
          <div className="p-4 border-t border-white/5 bg-gray-900/80 backdrop-blur-xl">
             <div className="relative group">
               <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl opacity-20 group-hover:opacity-100 transition duration-500 blur"></div>
               <div className="relative flex items-center bg-[#13161c] rounded-xl border border-white/10">
                 <input 
                   type="text" 
                   value={instruction}
                   onChange={(e) => setInstruction(e.target.value)}
                   onKeyDown={(e) => e.key === 'Enter' && handleRefine()}
                   placeholder="Ask AI to edit (e.g. 'Make it dark mode')"
                   className="w-full bg-transparent text-white pl-4 pr-12 py-3.5 focus:outline-none placeholder-gray-500 text-sm"
                   disabled={!generatedCode || isRefining}
                 />
                 <button 
                   onClick={handleRefine}
                   disabled={!instruction || isRefining}
                   className="absolute right-2 p-2 bg-indigo-600 rounded-lg text-white hover:bg-indigo-500 disabled:opacity-50 disabled:bg-gray-700 transition-all hover:scale-105"
                 >
                   {isRefining ? <Zap size={16} className="animate-spin"/> : <Send size={16} />}
                 </button>
               </div>
             </div>
             <p className="text-[10px] text-gray-500 mt-2 text-center font-medium">
               ✨ AI Context Aware • Powered by Gemini 3.0
             </p>
          </div>
        </div>

        {/* RIGHT COLUMN: Output */}
        <div className="flex-1 bg-[#0c0e12] flex flex-col min-w-0 relative">
          
          {/* Smart Loader Overlay */}
          {(isLoading || isRefining) && (
            <div className="absolute inset-0 z-50 bg-[#0c0e12]/80 backdrop-blur-md flex flex-col items-center justify-center animate-in fade-in duration-300">
               <div className="relative">
                 <div className="w-24 h-24 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"/>
                 <div className="absolute inset-0 flex items-center justify-center">
                   <Sparkles className="w-8 h-8 text-indigo-400 animate-pulse"/>
                 </div>
               </div>
               <h3 className="mt-8 text-xl font-bold text-white tracking-tight">Generating UI</h3>
               <p className="text-gray-400 mt-2 text-sm font-mono animate-pulse">{loadingStep}</p>
            </div>
          )}

          {/* Toolbar */}
          <div className="h-14 border-b border-white/5 flex items-center justify-between px-4 bg-gray-900/40 backdrop-blur-sm">
            <div className="flex bg-black/20 p-1 rounded-lg border border-white/5">
              <button 
                onClick={() => setActiveTab("preview")} 
                className={`flex items-center gap-2 px-4 py-1.5 rounded-md text-xs font-bold uppercase tracking-wider transition-all ${activeTab === 'preview' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}
              >
                <Monitor size={14} /> Preview
              </button>
              <button 
                onClick={() => setActiveTab("code")} 
                className={`flex items-center gap-2 px-4 py-1.5 rounded-md text-xs font-bold uppercase tracking-wider transition-all ${activeTab === 'code' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}
              >
                <Code size={14} /> Code
              </button>
            </div>

            <div className="flex items-center gap-2">
              {generatedCode && (
                <>
                  <button onClick={downloadCode} className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-colors border border-transparent hover:border-white/10">
                    <Download size={14} /> Export
                  </button>
                  <button onClick={copyToClipboard} className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20 hover:bg-green-500/20 transition-all">
                    {copied ? <Check size={14}/> : <Copy size={14}/>} {copied ? "Copied" : "Copy HTML"}
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Canvas Area */}
          <div className="flex-1 relative overflow-hidden">
            {!generatedCode ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-600 gap-6">
                <div className="w-24 h-24 rounded-full bg-white/5 border border-white/10 flex items-center justify-center animate-pulse">
                   <Monitor size={48} className="opacity-20"/>
                </div>
                <div className="text-center space-y-2">
                  <h3 className="text-xl font-medium text-gray-300">Ready to Create</h3>
                  <p className="text-gray-500 max-w-xs mx-auto">Upload a screenshot, wireframe, or napkin sketch to generate responsive code.</p>
                </div>
              </div>
            ) : (
              <>
                <div className={`w-full h-full ${activeTab === 'preview' ? 'block' : 'hidden'}`}>
                  <PreviewFrame htmlCode={generatedCode} />
                </div>
                <div className={`w-full h-full ${activeTab === 'code' ? 'block' : 'hidden'}`}>
                  <Editor
                    height="100%"
                    defaultLanguage="html"
                    theme="vs-dark"
                    value={generatedCode}
                    onChange={(val: string | undefined) => setGeneratedCode(val || "")}
                    options={{ 
                      minimap: { enabled: false }, 
                      fontSize: 14, 
                      fontFamily: 'JetBrains Mono, monospace',
                      padding: { top: 20 },
                      scrollBeyondLastLine: false,
                      smoothScrolling: true
                    }}
                  />
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
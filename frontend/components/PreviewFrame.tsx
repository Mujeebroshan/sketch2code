"use client";
import React, { useEffect, useState } from 'react';

interface PreviewFrameProps {
  htmlCode: string;
}

export default function PreviewFrame({ htmlCode }: PreviewFrameProps) {
  const [iframeSrc, setIframeSrc] = useState<string>('');

  useEffect(() => {
    if (!htmlCode) return;
    const blob = new Blob([htmlCode], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    setIframeSrc(url);
    return () => URL.revokeObjectURL(url);
  }, [htmlCode]);

  if (!iframeSrc) return null;

  return (
    <iframe 
      src={iframeSrc}
      className="w-full h-full border-0 rounded-xl shadow-sm bg-white"
      sandbox="allow-scripts"
    />
  );
}
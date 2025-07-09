import React, { useState, useCallback } from 'react';
import { BiUpload, BiFile, BiX, BiCloudUpload } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation } from '../../utils/translations';

interface FileDropZoneProps {
  onFileUpload: (file: File) => Promise<void>;
  isUploading: boolean;
  onCancel: () => void;
}

const FileDropZone: React.FC<FileDropZoneProps> = ({
  onFileUpload,
  isUploading,
  onCancel
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragOver(true);
    }
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    // Only set to false if we're actually leaving the drop zone
    if (!e.currentTarget.contains(e.relatedTarget as Node)) {
      setIsDragOver(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      const file = files[0];
      if (file.type === 'application/pdf') {
        onFileUpload(file);
      } else {
        alert(t('chat.pdf_only'));
      }
    }
  }, [onFileUpload, t]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type === 'application/pdf') {
        onFileUpload(file);
      } else {
        alert(t('chat.pdf_only'));
      }
    }
  }, [onFileUpload, t]);

  return (
    <div className="flex-1 flex flex-col h-full bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-200/10 to-purple-200/10 dark:from-blue-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-purple-200/10 to-blue-200/10 dark:from-purple-500/10 dark:to-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Header */}
      <div className="flex items-center justify-between p-6 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl border-b border-gray-200/60 dark:border-slate-700/60 relative z-10">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 bg-gradient-to-br from-blue-500 to-indigo-600 dark:from-blue-400 dark:to-indigo-500 rounded-xl flex items-center justify-center shadow-lg">
            <BiCloudUpload className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">{t('chat.upload_document')}</h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">{t('chat.upload_document_subtitle')}</p>
          </div>
        </div>
        <button
          onClick={onCancel}
          className="p-2 rounded-xl bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 transition-all duration-200 text-gray-600 dark:text-gray-300"
        >
          <BiX className="h-5 w-5" />
        </button>
      </div>

      {/* Drop Zone */}
      <div className="flex-1 flex items-center justify-center p-8 relative z-10">
        <div
          className={`w-full max-w-2xl mx-auto relative ${
            isDragOver ? 'scale-105' : 'scale-100'
          } transition-all duration-300`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div
            className={`border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 ${
              isDragOver
                ? 'border-blue-500 bg-blue-50/80 dark:bg-blue-900/20 shadow-2xl'
                : 'border-gray-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 hover:border-blue-400 dark:hover:border-blue-500 hover:bg-blue-50/50 dark:hover:bg-blue-900/10'
            } backdrop-blur-xl shadow-xl`}
          >
            {isUploading ? (
              <div className="space-y-6">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent mx-auto"></div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {t('chat.uploading_processing')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    {t('chat.please_wait')}
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="relative">
                  <div className="h-16 w-16 bg-gradient-to-br from-blue-500 to-indigo-600 dark:from-blue-400 dark:to-indigo-500 rounded-2xl flex items-center justify-center mx-auto shadow-lg">
                    <BiUpload className="h-8 w-8 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 h-6 w-6 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
                    <BiFile className="h-3 w-3 text-white" />
                  </div>
                </div>
                
                <div className="space-y-3">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {t('chat.drag_drop_pdf')}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-lg">
                    {t('chat.or_select_file')}{' '}
                    <label className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 cursor-pointer font-semibold underline underline-offset-2">
                      {t('common.select')}
                      <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileSelect}
                        className="hidden"
                      />
                    </label>
                  </p>
                </div>

                <div className="bg-gray-50 dark:bg-slate-700/50 rounded-xl p-4 space-y-2">
                  <div className="flex items-center justify-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                    <BiFile className="h-4 w-4" />
                    <span>{t('chat.pdf_only')}</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                    <BiUpload className="h-4 w-4" />
                    <span>{t('chat.max_file_size')}</span>
                  </div>
                </div>

                <div className="text-xs text-gray-500 dark:text-gray-400">
                  {t('chat.file_secure')}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileDropZone;

// components/UploadForm.tsx
"use client";

import { useCallback, useState } from 'react';
import axios from 'axios';
import { useDropzone, DropzoneOptions } from 'react-dropzone';
import Loading from './Uploading';


function UploadForm() {
    const [file, setFile] = useState<File | null>(null);

    const [loading, setLoading] = useState<boolean>(false);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles && acceptedFiles.length > 0) {
            setFile(acceptedFiles[0]);
        }
    }, []);

    const dropzoneOptions: DropzoneOptions = {
        onDrop,
        multiple: false,
        onDragEnter: () => console.log('Drag enter'),
        onDragOver: () => console.log('Drag over'),
        onDragLeave: () => console.log('Drag leave'),
    };

    const { getRootProps, getInputProps } = useDropzone(dropzoneOptions);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        // const formData = new FormData();
        // formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData);
            alert(response.data.message);
        } catch (error) {
            console.error('Error uploading file', error);
        } finally {
            setLoading(false);
        }
    };


    return (
        <form onSubmit={handleSubmit} className="flex flex-col items-center">
            <div
                {...getRootProps()}
                className="flex justify-center items-center w-100 h-48 border-2 border-dashed border-gray-400 rounded-md bg-gray-50 cursor-pointer transition-all duration-300 hover:border-gray-600"
            >
                <input {...getInputProps()} className="hidden" />
                {file ? (
                    <p>{file.name}</p>
                ) : (
                    <p>Drag 'n' drop some files here, or click to select files</p>
                )}
            </div>
            <button type="submit" className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-all duration-300">
                Upload
            </button>
            {loading && <Loading />}
        </form>
    );
}

export default UploadForm;

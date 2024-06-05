// components/Loading.tsx
import React from 'react';

const Loading: React.FC = () => {
    return (
        <div className="flex justify-center items-center h-full">
            <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-32 w-32"></div>
        </div>
    );
};

export default Loading;

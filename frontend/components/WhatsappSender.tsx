import React from 'react';

const WhatsAppSender: React.FC = () => {
  const whatsappLink = "https://api.whatsapp.com/send/?text=Selamat%20pagi,%0A%0ABerikut%20kami%20informasikan%20terkait%20Upload%20Dasboard%20tanggal%206%20Juni%202024%20-%2008%3A28%3A10%20WIB,%20sudah%20berhasil%0A%0ADemikian%20disampaikan,%20atas%20perhatian%20dan%20kerjasamanya%20kami%20ucapankan%20terimakasih%0A%0ASalam%0A%0AAhmad%20Rafi%20Rusydi";
  const whatsappImage = "https://api.whatsapp.com/send/?image="
  return (
    <a href={whatsappLink} target="_blank" rel="noopener noreferrer" className="inline-block bg-green-500 px-4 py-2 rounded-md text-white shadow-md transition duration-300 ease-in-out transform hover:scale-105">
      <i className="fadeIn animated bx bx-share-alt mr-2"></i> Kirim WA
    </a>
  );
};

export default WhatsAppSender;

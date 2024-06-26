import Image from "next/image";
import UploadForm from "@/components/UploadForm";
// import DataView from "@/components/DataView";

import WhatsAppSender from "@/components/WhatsappSender";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div>
        <UploadForm />
      </div>
        
      <div>
        <WhatsAppSender />
      </div>
    </main>
  );
}

"use client";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { User } from "lucide-react";
import Cookies from "js-cookie";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { QRScanner } from "@/components/ui/qrscanner";
import { useSearchParams } from "next/navigation";


interface FoodItem {
  name: string;
  price: number;
  image: string;
}

export default function SmartFridgeEcommerce() {
  const [activeTab, setActiveTab] = useState("browse");
  const [foodItems, setFoodItems] = useState([]);
  const [sensor, setSensor] = useState({
    temperatura: '',
    humedad: ''
  })
  const searchParams = useSearchParams();
  const [redirectStartSession,setRedirectStartSession] = useState(false)//searchParams.get('redirectStartSession');

  const checkUserCard = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}payment/check-card/`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${Cookies.get("authToken")}`, // Usa el token guardado en cookies
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Error en la respuesta de la API");
      }

      const data = await response.json();
      if (!data.has_card) {
        if (redirectStartSession) {
          window.location.href = "/cards/add?homeRedirect=true&redirectStartSession=true";
        } else {
          window.location.href = "/cards/add?homeRedirect=true";
        }
      } else {
        console.error("El usuario tiene tarjeta...");
      }
    } catch (error) {
      console.error("Error en la peticion", error);
    }
  };

  const downloadProducts = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}market/fridge/1/products/list/`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${Cookies.get("authToken")}`, // Usa el token guardado en cookies
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Error en la respuesta de la API");
      }
      console.log(response)

      const data = await response.json();
      console.log(data)
      setFoodItems(data)
    } catch (error) {
      console.error("Error en la peticion", error);
    }
  };
  const obtenerDatosSensor = async () => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}market/fridge/sensar/`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${Cookies.get("authToken")}`, // Usa el token guardado en cookies
          "Content-Type": "application/json",
        },
      }
    )
    const data = await response.json();
    setSensor({
      ...sensor,
      temperatura: data.Temperatura,
      humedad: data.humedad
    })
  }
  useEffect(() => {
    const intervalo = setInterval(() => {
      obtenerDatosSensor();
      console.log("me estoy ejecutando ")
    },1000*60)
    return () => {
      console.log("Intervalo limpiado")
      clearInterval(intervalo);
    }
  },[])
  useEffect(() => {
    downloadProducts();
    checkUserCard();
  }, []);

  const handleLogout = () => {
    // Eliminar todas las cookies
    const allCookies = Cookies.get(); // Obtener todas las cookies actuales
    // Recorrer y eliminar cada cookie
    for (let cookie in allCookies) {
      Cookies.remove(cookie);
    }
    // Redirigir al usuario a la pgina de inicio de sesion
    window.location.href = "/login";
  };

  const handleAddCreditCard = () => {
    window.location.href = "/cards";
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Smart Fridge Eats
          </h1>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" onClick={handleAddCreditCard}>
              <Card className="mr-2 h-4 w-4" />
              Credit Cards
            </Button>
            <Button variant="ghost" onClick={handleLogout}>
              <User className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
          <div className="flex flex-col">
            <span>Temperatura: {sensor.temperatura} C </span>
            <span> Humedad: {sensor.humedad} %</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsContent value="browse">
              <div className="flex flex-col items-center justify-center">
                <Button onClick={()=>{setRedirectStartSession(!redirectStartSession)
                  window.location.href="/qr-scan/1"
                }}>Iniciar compra</Button>
              </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
              {foodItems.map((item: any) => ( 
                <Card 
                  key={item.name}> 
                <CardHeader> 
                    <CardTitle>{item.name}</CardTitle> 
                    <CardDescription>${item.price.toFixed(2)}</CardDescription> 
                </CardHeader> 
                <CardContent> 
                  <img 
                   src={item.image} 
                   alt={item.name} 
                   className="w-full h-40 object-cover rounded-md" 
                  /> 
                </CardContent> 
              </Card>
               ))}
            </div>
          </TabsContent>
          <TabsContent value="qr-scanner">
            <Card>
              <CardHeader>
                <CardTitle>Scan QR Code</CardTitle>
                <CardDescription>
                  Use your device's camera to scan a QR code
                </CardDescription>
              </CardHeader>
              <CardContent>
                <QRScanner />
              </CardContent>
            </Card>
          </TabsContent>
          {/* <TabsContent value="map">
            <Card>
              <CardHeader>
                <CardTitle>Dark Mode Map</CardTitle>
                <CardDescription>
                  Google Maps in dark mode with zoom level 14
                </CardDescription>
              </CardHeader>
              <CardContent>
                <DarkModeMap />
              </CardContent>
            </Card>
          </TabsContent> */}
        </Tabs>
      </main>
    </div>
  );
}

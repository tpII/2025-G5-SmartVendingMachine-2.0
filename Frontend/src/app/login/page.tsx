"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { LogIn } from "lucide-react";
import Cookies from "js-cookie";
import { useSearchParams } from 'next/navigation';

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const searchParams = useSearchParams();
  const redirectStartSession =/*true*/  searchParams.get('redirectStartSession');


  const handleLogin = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}api/login/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username,
            password: password,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();

        // Supongamos que el token está en data.token
        console.log(data);
        Cookies.set("authToken", data.access, { expires: 7 }); // La cookie expira en 7 días
        alert("Login exitoso!");
        console.log("Login exitoso");
        console.log("redirectStartSession", redirectStartSession)
        if (redirectStartSession) {
          window.location.href = "/qr-scan/1";
        } else {
          window.location.href = "/";
        }
      } else {
        console.error("Error en el login");
        alert("Hubo un error al iniciar sesión!");
      }
    } catch (error) {
      alert("Hubo un error al iniciar sesión!");
      console.error("Error en la petición", error);
    }
  };

  const handleSignUpEvent = () => {
    if (redirectStartSession) {
      window.location.href = "/sign-up?redirectStartSession=true";
    } else {
      window.location.href = "/sign-up";
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Smart Fridge Eats</h1>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" onClick={handleSignUpEvent}>
              <LogIn className="mr-2 h-4 w-4" />
              Sign Up
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Login</CardTitle>
            <CardDescription>
              Access your account or create a new one
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Email"
              type="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button className="w-full" onClick={handleLogin}>
              Login
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

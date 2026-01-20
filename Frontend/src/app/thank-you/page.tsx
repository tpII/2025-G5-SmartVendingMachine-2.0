'use client'

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CheckCircle, ShoppingBag } from "lucide-react";
import Link from "next/link";

interface ProductDetails {
  precio: number;
  stock_anterior: number;
  cantidad_retirada: number;
  stock_actual: number;
}

interface ProductosInfo {
  [productName: string]: ProductDetails;
}

interface ProductsResponse {
  productos_info: ProductosInfo;
}

const productNameMapping: Record<string, string> = {
  "oreo": "Oreo",
  "pepsi": "Pepsi",
  "lays": "Lay's",
};

export default function ThankYouPage() {
  const [productsInfo, setProductsInfo] = useState<ProductsResponse | null>(null);

  useEffect(() => {
    try {
      const data = localStorage.getItem("productsInfo");
      if (data) {
        setProductsInfo(JSON.parse(data));
      }
    } catch (error) {
      console.error("Error al cargar los datos del localStorage:", error);
    }
  }, []);

  if (!productsInfo) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <CheckCircle className="mx-auto h-16 w-16 text-green-500" />
          <h1 className="mt-4 text-3xl font-extrabold text-gray-900">
            Gracias por su compra
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Su transacción ha sido realizada exitosamente.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Resumen de Productos</CardTitle>
            <CardDescription>
              Detalles de los productos retirados de la heladera.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Producto</TableHead>
                  <TableHead>Precio</TableHead>
                  <TableHead>Cantidad Retirada</TableHead>
                  <TableHead>Stock Anterior</TableHead>
                  <TableHead>Stock Actual</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(productsInfo.productos_info).map(
                  ([productName, details], index) => (
                    <TableRow key={index}>
                      <TableCell>{productNameMapping[productName] || productName}</TableCell>
                      <TableCell>${details.precio.toFixed(2)}</TableCell>
                      <TableCell>{details.cantidad_retirada}</TableCell>
                      <TableCell>{details.stock_anterior}</TableCell>
                      <TableCell>{details.stock_actual}</TableCell>
                    </TableRow>
                  )
                )}
              </TableBody>
            </Table>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button asChild className="w-full">
              <Link href="/">
                <ShoppingBag className="mr-2 h-4 w-4" />
                Volver al menú
              </Link>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

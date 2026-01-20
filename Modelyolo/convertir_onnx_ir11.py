import onnx

# Rutas (usando raw string)
input_model = r"C:\Users\josep\OneDrive\Desktop\Pruebamodel\nuevobestna.onnx"
output_model = r"C:\Users\josep\OneDrive\Desktop\Pruebamodel\nuevobestna_ir11.onnx"

# Cargar el modelo
model = onnx.load(input_model)

# Cambiar la versión del IR a 7 (compatible con IR v11 de ONNXRuntime)
model.ir_version = 7

# Guardar el modelo nuevo
onnx.save(model, output_model)

print(f"Modelo convertido guardado como {output_model}")

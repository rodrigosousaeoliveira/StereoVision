from flask import Flask, render_template
import time

start = time.perf_counter()

app = Flask(__name__)

index = """
 <!DOCTYPE html>
<html>
<head>
<title>StereoVision</title>
</head>
<body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1)

    const renderer = new THREE.WebGLRenderer()
    renderer.setSize(window.innerWidth-100, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    const box = new THREE.BoxGeometry(1,1,1)
    const material  = new THREE.MeshBasicMaterial({ color: 0xff0000})
    
    const cube = new THREE.Mesh(box, material)

    scene.add(cube)

    const animate = () => {

        requestAnimationFrame( animate)

        cube.rotation.x += 0.05
        cube.rotation.y += 0.01
        cube.rotation.z += 0.01
        
        camera.position.z = 5
        renderer.render(scene, camera)
    }
    animate()
    

</script>

</body>
</html> 
"""

@app.route("/")
def hello_world():
    return index

while True:
    now = time.perf_counter()-start
    app.run()
    if now < 10:
        print('hello')
        break
    
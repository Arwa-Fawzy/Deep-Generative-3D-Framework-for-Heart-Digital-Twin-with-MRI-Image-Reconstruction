import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xF0F0F0);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, -6, 50); // Moved slightly down

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);

// Append Renderer to Container
document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("container3D");
    if (!container) {
        console.error("Error: #container3D not found!");
        return;
    }
    container.appendChild(renderer.domElement);
});

// Orbit Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Lighting
const mainLight = new THREE.DirectionalLight(0xffffff, 2);
mainLight.position.set(500, 500, 500);
scene.add(mainLight);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const backLight = new THREE.DirectionalLight(0xffffff, 1);
backLight.position.set(-500, -500, -500);
scene.add(backLight);

let mixer;

// Load 3D Model
const loader = new GLTFLoader();
loader.load(
    "http://localhost:8002/models/Heart.glb",
    function (gltf) {
        const object = gltf.scene;

        // Create a parent group to control relative positioning
        const parentGroup = new THREE.Group();
        parentGroup.add(object);

        // Now you can position the group relative to the scene
        parentGroup.position.set(0, -5, 0);
        parentGroup.scale.set(1.5, 1.5, 1.5);

        scene.add(parentGroup);

        // Setup animations
        if (gltf.animations.length > 0) {
            mixer = new THREE.AnimationMixer(object); // Still reference the original object
            gltf.animations.forEach((clip) => {
                const action = mixer.clipAction(clip);
                action.play();
            });
            console.log("Animations found and playing.");
        } else {
            console.warn("No animations found in the model.");
        }
    },
    function (xhr) {
        console.log(`Loading: ${(xhr.loaded / xhr.total) * 100}%`);
    },
    function (error) {
        console.error("Error loading model:", error);
    }
);

// Animation Loop
function animate() {
    requestAnimationFrame(animate);
    if (mixer) mixer.update(0.01);
    renderer.render(scene, camera);
}

animate();

// Handle Window Resize
window.addEventListener("resize", function () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

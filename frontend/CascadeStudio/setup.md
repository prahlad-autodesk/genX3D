To install and run **Cascade Studio locally**, follow the steps below. It's a lightweight BRep (OpenCascade) CAD modeler in the browser, using WebAssembly via `opencascade.js`.

---

## ✅ 1. Clone the Repository

```bash
git clone https://github.com/zalo/CascadeStudio.git
cd CascadeStudio
```

---

## ✅ 2. Install Dependencies

CascadeStudio uses **Node.js + npm** for dependency management.

> 🟡 Minimum Node.js version: **12+**
> ✅ Recommended: Node.js **16 or 18**

Install dependencies:

```bash
npm install
```

---

## ✅ 3. Run the Development Server

This will start a local web server and open the app in your browser:

```bash
npm start
```

This runs `node server.js`, which hosts the `index.html` and associated files.

You can now open your browser and go to:

```
http://localhost:8000
```

---

## ✅ 4. (Optional) Build a Production Bundle

If you want to deploy Cascade Studio as a static site:

```bash
npm run build
```

It will bundle everything into a `dist/` or similar directory (depending on config).

---

## 🧠 What Happens Behind the Scenes

* Uses **`opencascade.js`**: WebAssembly-compiled version of OpenCascade
* Editor: **Monaco Editor** (like VSCode)
* 3D Renderer: **Three.js**
* Loads and runs all geometry in your browser — no backend needed

---

## 🔧 Trouble?

If `npm start` fails:

* Ensure you're in the root of the cloned repo (where `package.json` exists)
* Try deleting `node_modules` and reinstalling:

```bash
rm -rf node_modules
npm install
```

---

## ✅ Summary

| Step | Command                                                      |
| ---- | ------------------------------------------------------------ |
| 1    | `git clone https://github.com/zalo/CascadeStudio.git`        |
| 2    | `cd CascadeStudio`                                           |
| 3    | `npm install`                                                |
| 4    | `npm start` → [http://localhost:8000](http://localhost:8000) |

---

Let me know if you want to:

* Run it inside Docker
* Integrate it with a Python/CadQuery backend
* Serve it via FastAPI or Nginx

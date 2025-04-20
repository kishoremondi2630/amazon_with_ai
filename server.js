const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// Set up storage for images
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/'); // Directory where files will be saved
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${file.originalname}`;
    cb(null, uniqueName);
  },
});

// Multer middleware
const upload = multer({ storage: storage });

// Serve static files from the "uploads" folder
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Endpoint to handle image upload
app.post('/upload', upload.array('images', 3), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: 'No files uploaded' });
  }

  // Return the file paths of the saved images
  const filePaths = req.files.map((file) => `/uploads/${file.filename}`);
  res.json({ message: 'Images uploaded successfully', files: filePaths });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

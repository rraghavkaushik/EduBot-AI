# EduBot Frontend

A modern, professional React frontend for the EduBot AI-powered learning platform.

## ✨ Features

### 🎨 **Modern Design System**
- **Professional UI/UX**: Clean, modern interface designed for educational use
- **Responsive Design**: Mobile-first approach with tablet and desktop optimization
- **CSS Variables**: Consistent color scheme and design tokens
- **Smooth Animations**: Subtle hover effects and page transitions
- **Gradient Accents**: Beautiful visual elements throughout the interface

### 🚀 **Enhanced Functionality**
- **Authentication System**: Secure login/register with JWT tokens
- **File Upload**: Drag-and-drop file upload with progress tracking
- **Document Management**: View and manage uploaded documents
- **Real-time Status**: Live backend connectivity status
- **Form Validation**: Client-side validation with error handling

### 📱 **User Experience**
- **Loading States**: Smooth loading animations and progress indicators
- **Error Handling**: User-friendly error messages and recovery
- **Navigation**: Intuitive navigation with active state indicators
- **Accessibility**: Semantic HTML and keyboard navigation support

## 🛠️ Technology Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing and navigation
- **Vite**: Fast build tool and development server
- **CSS3**: Modern CSS with custom properties and Grid/Flexbox
- **Axios**: HTTP client for API communication
- **Local Storage**: Token persistence and session management

## 🎯 **Pages & Components**

### **Home Page** (`/`)
- Hero section with call-to-action buttons
- Feature showcase with icons and descriptions
- How-it-works step-by-step guide
- System status indicator
- Responsive grid layout

### **Register Page** (`/register`)
- Professional registration form
- Real-time form validation
- Password strength requirements
- Feature benefits showcase
- Link to login page

### **Login Page** (`/login`)
- Clean authentication form
- Demo account credentials
- Error handling and feedback
- Link to registration
- Secure token management

### **Upload Page** (`/upload`)
- Drag-and-drop file upload
- File type validation (PDF, TXT)
- Upload progress tracking
- File preview and management
- Uploaded files history
- Helpful tips and guidelines

### **Header Component**
- Responsive navigation
- Authentication state management
- Active page indicators
- Brand logo with gradient text
- Mobile-friendly design

## 🎨 **Design System**

### **Color Palette**
- **Primary**: Indigo gradient (`#6366f1` → `#4f46e5`)
- **Secondary**: Purple gradient (`#8b5cf6`)
- **Accent**: Cyan gradient (`#06b6d4`)
- **Success**: Green (`#10b981`)
- **Error**: Red (`#ef4444`)
- **Warning**: Amber (`#f59e0b`)

### **Typography**
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800
- **Hierarchy**: Clear heading and text styles
- **Readability**: Optimized line heights and spacing

### **Components**
- **Cards**: Elevated with shadows and hover effects
- **Buttons**: Gradient backgrounds with hover animations
- **Forms**: Clean inputs with focus states
- **Icons**: Emoji-based icons for visual appeal
- **Grids**: Responsive layout system

## 🚀 **Getting Started**

### **Prerequisites**
- Node.js 18+ 
- npm or yarn

### **Installation**
```bash
cd frontend
npm install
```

### **Development**
```bash
npm run dev
```
The app will be available at `http://localhost:5174`

### **Build**
```bash
npm run build
```

## 📱 **Responsive Breakpoints**

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🔧 **Configuration**

### **Environment Variables**
- `VITE_API_BASE_URL`: Backend API base URL
- `VITE_APP_TITLE`: Application title

### **API Integration**
- Automatic token management
- Request/response interceptors
- Error handling and retry logic

## 🎭 **Animations & Transitions**

- **Page Transitions**: Fade-in animations
- **Hover Effects**: Button and card interactions
- **Loading States**: Spinner animations
- **Progress Bars**: Upload progress visualization

## 🔒 **Security Features**

- **JWT Authentication**: Secure token-based auth
- **Token Persistence**: Local storage with automatic cleanup
- **Protected Routes**: Authentication-required pages
- **Input Validation**: Client-side form validation

## 📊 **Performance Features**

- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component lazy loading
- **Optimized Images**: SVG icons and optimized assets
- **CSS Optimization**: Minimal CSS with utility classes

## 🧪 **Testing**

The frontend is designed with testability in mind:
- Component isolation
- Prop-based state management
- Mock-friendly API calls
- Accessible component structure

## 🌟 **Future Enhancements**

- **Dark Mode**: Theme switching capability
- **Offline Support**: Service worker implementation
- **Real-time Updates**: WebSocket integration
- **Advanced Analytics**: User behavior tracking
- **Multi-language**: Internationalization support

## 📝 **Contributing**

1. Follow the existing code style
2. Use semantic commit messages
3. Test on multiple devices
4. Ensure accessibility compliance
5. Update documentation as needed

## 📄 **License**

This project is part of the EduBot platform and follows the same licensing terms.

---

**Built with ❤️ for educational excellence**

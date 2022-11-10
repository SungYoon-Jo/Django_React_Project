import {Route, Routes} from 'react-router-dom';
import Home from './pages/Home.js';
import Find from './pages/Find.js';

const App = () => {
  return(
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/find" element={<Find />} />
    </Routes>
  );
};

export default App;
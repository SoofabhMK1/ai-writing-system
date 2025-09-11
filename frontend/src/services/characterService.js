import api from './api';

const characterService = {
  getCharacters() {
    return api.get('/characters/');
  },
  createCharacter(characterData) {
    return api.post('/characters/', characterData);
  },
};

export default characterService;

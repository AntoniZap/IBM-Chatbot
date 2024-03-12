import React from 'react';
import JaedonSWENG from '../assets/JaedonSWENG.jpg';
import DellaSWENG from '../assets/DellaSweng.jpg';
import NicSweng from '../assets/NicSweng.jpg'; 
import EmmeliaSweng from '../assets/EmmeliaSweng.jpg';
import Sprina from '../assets/SprinaSweng.jpg';
import Darragh from '../assets/DarraghSweng.jpg';
import Sean from '../assets/SeanSweng.jpg';
import Antoni from '../assets/AnptoniSweng.png';
import Nozz from '../assets/NozzSweng.png';
import Lorca from '../assets/LorcaSweng.png';
import Dylan from '../assets/DylanSweng.jpg';
import './AboutUs.css'; // Import the CSS file

const teamMembers = [
  { name: 'Jaedon', role: 'Frontend Lead', about: 'I am a 3rd year ICS student here at Trinity. For this project I was tasked with the development of the frontend. I thoroughly enjoyed my time with the group and with IBM.', image: JaedonSWENG },
  { name: 'Della', role: 'Backend Lead', about: 'I am a 3rd Year ICS Student at Trinity College Dublin. For this project I was tasked with leading the vector store and database team in the backend. I also worked alongside the frontend team. The process of working alongside IBM was ENJOYABLE, challenging and informative.', image: DellaSWENG},
  { name: 'Nicolas', role: 'Backend', about: 'My name is Nicholas and I am a second year computer science student at Trinity. On this project I am working on the chunking team which will help to handle extremely large datasets.', image: NicSweng }, 
  { name: 'Sprina', role: 'Frontend', about: 'I am a third year Computer Science and Business student here at Trinity College Dublin. I have enjoyed working for our front end of the SwEng project on behalf of IBM!', image: Sprina },
  { name: 'Darragh', role: 'Team Lead', about: 'I am a Third Year ICS student here at Trinity College Dublin. I am loving working as a Team Lead for our SwEng project on behalf of our client Abhay Chaudhary of IBM. I am excited to be building our customer reviews chatbot, "FeedBot", as part of an amazing team!', image: Darragh },
  { name: 'Emmelia', role: 'Backend & Social Media', about: 'I am a second year ICS student at Trinity College Dublin. My role spans the testing and LLM team in the backend, as well as the social media team. Working alongside IBM has been not only enlightening, but above all enjoyable.', image: EmmeliaSweng },
  { name: 'Seán', role: 'File Processing & Social Media', about: 'I am a second year ICS student at Trinity College Dublin. I am a member of the chunking team, as well as working on the social media team.  Working on this project alongside my team has been a great experience that will be invaluable in the future.', image: Sean },
  { name: 'Antoni', role: 'Backend Lead', about: 'I am a Third Year Computer Science student at Trinity College Dublin. Working in and helping manage a team, which is creating an interesting software, gives a lot of pleasure, fun and experience!', image: Antoni },
  { name: 'Chinaza', role: 'Backend Lead', about: 'I am a a third year computer science student at Trinity. On this project I work with the backend team writing code to allow the user to process thousands of product reviews with natural language questions.', image: Nozz },
  { name: 'Lorca', role: 'Backend', about: 'My name is Lorca and I am a second year computer science and business student at Trinity. I’m a member of the llm and unit testing teams. I’ve enjoyed working alongside my team for our client IBM and have gained valuable experience so far.', image: Lorca },
  { name: 'Dylan', role: 'Backend & Social Media', about: 'My name is Dylan and I am a 2nd year ICS student at Trinity. I am part of the query team as well as running the social media. Working with my team thus far has given invaluable experience for the future.', image: Dylan },
  // Add additional members as needed...
];

function AboutUs() {
  return (
    <div className="member-container">
      {teamMembers.map((member) => (
        <div key={member.name} className="member"> {/* Changed key to member.name for uniqueness */}
          <img src={member.image} alt={member.name} className="profile-icon" />
          <h2 className="member-name">{member.name}</h2>
          <h3 className="member-role">{member.role}</h3>
          <p className="member-about">{member.about}</p>
        </div>
      ))}
    </div>
  );
}

export default AboutUs;

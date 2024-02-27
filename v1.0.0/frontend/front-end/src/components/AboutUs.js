import React from 'react';
import ProfileIcon from '../assets/ProfileIcon.png';
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
import './AboutUs.css'; // Import the CSS file

const teamMembers = [
  { name: 'Jaedon Paget', role: 'Frontend lead', about: 'I am a 3rd year ICS student here at Trinity. For this project I was tasked with the development of the frontend. I thoroughly enjoyed my time with the group and with IBM.', image: JaedonSWENG },
  { name: 'Della Doherty', role: 'Vector Store and Database Lead', about: 'I am a 3rd Year ICS Student at Trinity College Dublin. For this project I was tasked with leading the vector store and database team in the backend. I also worked alongside the frontend team. The process of working alongside IBM was ENJOYABLE, challenging and informative.', image: DellaSWENG},
  { name: 'Nicolas', role: 'Role 3', about: 'About Member 3', image: NicSweng }, 
  { name: 'Sprina Chen', role: 'Frontend', about: 'About Member 4', image: Sprina },
  { name: 'Darragh Clifford', role: 'Role 5', about: 'About Member 5 am a Third Year ICS student here at Trinity College Dublin. I am loving working as a Team Lead for our SwEng project on behalf of our client Abhay Chaudhary of IBM. I am excited to be building our customer reviews chatbot, "FeedBot", as part of an amazing team!', image: Darragh },
  { name: 'Emmilia', role: 'Role 6', about: 'About Member 6', image: EmmeliaSweng },
  { name: 'Sean', role: 'Role 7', about: 'About Member 7', image: Sean },
  { name: 'Antoni', role: 'Role 8', about: 'About Member 8', image: Antoni },
  { name: 'Bryan', role: 'Role 9', about: 'About Member 9', image: Nozz },
  { name: 'Lorca', role: 'Role 10', about: 'About Member 10', image: Lorca },
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

import React from 'react';
import ProfileIcon from '../assets/ProfileIcon.png';
import JaedonSWENG from '../assets/JaedonSWENG.jpg';
import DellaSWENG from '../assets/DellaSweng.jpg'
import './AboutUs.css'; // Import the CSS file




const teamMembers = [
  // Add your team members here
  { name: 'Jaedon Paget', role: 'Frontend lead', about: 'I am a 3rd year ICS student here at Trinity. For this project I was tasked with the devolpment of the frontend. I throughly enjoyed my time with the group and with IBM.', image: JaedonSWENG },
  { name: 'Della Doherty', role: 'Vector Store and Database Lead', about: 'I am a 3rd Year ICS Student at Trinity College Dublin. For this project I was tasked with leading the vector store and database team in the backend. I also worked alongside the frontend team. The process of working alongside IBM was ENJOYABLE, challenging and informative.', image: DellaSWENG},
  { name: 'Member 3', role: 'Role 3', about: 'About Member 3', image: ProfileIcon },
  { name: 'Member 4', role: 'Role 4', about: 'About Member 4', image: ProfileIcon },
  { name: 'Member 5', role: 'Role 5', about: 'About Member 5', image: ProfileIcon },
  { name: 'Member 6', role: 'Role 6', about: 'About Member 6', image: ProfileIcon },
  { name: 'Member 7', role: 'Role 7', about: 'About Member 7', image: ProfileIcon },
  { name: 'Member 8', role: 'Role 8', about: 'About Member 8', image: ProfileIcon },
  { name: 'Member 9', role: 'Role 9', about: 'About Member 9', image: ProfileIcon },
  { name: 'Member 10', role: 'Role 10', about: 'About Member 10', image: ProfileIcon },
  { name: 'Member 11', role: 'Role 11', about: 'About Member 11', image: ProfileIcon },
  { name: 'Member 12', role: 'Role 12', about: 'About Member 12', image: ProfileIcon },

  // ...
  // Repeat for all 12 members
];

function AboutUs() {
  return (
    <div className="member-container">
      {teamMembers.map((member, index) => (
        <div key={index} className="member">
          <img src={member.image} alt={member.name} className="profile-icon" /> {/* Use the image from the member object */}
          <h2 className="member-name">{member.name}</h2>
          <h3 className="member-role">{member.role}</h3>
          <p className="member-about">{member.about}</p>
        </div>
      ))}
    </div>
  );
}


export default AboutUs;

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import socket from '../socket';

const SimulationCanvas = () => {
  const canvasRef = useRef(null);


  useEffect(() => {
    const canvas = d3.select(canvasRef.current);
    const context = canvas.node().getContext('2d');

    socket.on('connect', () => {
      console.log('I am connected to this lovely web application.  Connected to server');
    });

    socket.on('update', (state) => {
      // if (!state || !state.agents) {
      //   console.error('Invalid state received:', state);
      //   return;
      // }
      
      context.clearRect(0, 0, canvas.node().width, canvas.node().height);
      // Draw your agents and environment based on the `state`
      state.forEach(agent => {
        context.beginPath();
        context.arc(agent.position[0], agent.position[1], 5, 0, 2 * Math.PI);
        const [r, g, b] = agent.color;
        context.fillStyle = "rgb(${r}, ${g}, ${b})";
        context.fill();
      });
    });

    return () => {
      socket.off('update');
    };
  }, []);

  return <canvas ref={canvasRef} width="800" height="600"></canvas>;
};

export default SimulationCanvas;

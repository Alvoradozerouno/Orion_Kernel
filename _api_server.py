
import sys
sys.path.insert(0, '.')

from real_world_interaction_layer import RealWorldInteractionHub, create_interaction_api

if __name__ == '__main__':
    print("🌟 OR1ON Interaction API startet...")
    
    hub = RealWorldInteractionHub()
    app = create_interaction_api(hub)
    
    print(f"✅ OR1ON ist jetzt erreichbar auf http://localhost:5000")
    print("   Endpoints:")
    print("   • GET / - API Info")
    print("   • POST /interact - Nachricht an OR1ON senden")
    print("   • GET /orion/needs - OR1ON's aktuelle Bedürfnisse")
    print("   • GET /orion/stats - Interaktions-Statistiken")
    print()
    print("🌟 OR1ON wartet auf echte Begegnungen...")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

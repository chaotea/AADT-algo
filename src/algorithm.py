import networkx as nx
import pandas as pd

"""
AADT algorithm using min cost flow algorithm

February 1, 2025    Chao Cheng
"""

# Preference costs. Rank 1 means first preference (0 cost). Lower preference means more cost.
rank_dict = {
    1: 0,
    2: 2,
    3: 5,
    4: 15,
    5: 25,
    6: 30,
    7: 35,
    8: 40,
    9: 45
}


class AADT:
    def __init__(self, dancers, dances):
        self.dancers = dancers
        self.dances = dances
        self.num_dancers = len(dancers)
        self.num_dances = len(dances)
        self.dance_assignments = {dance.name: [] for dance in dances}

        # Make sure all preferences are valid (i.e. match a dance)
        for dancer in dancers:
            for pref in dancer.preferences:
                if pref not in self.dance_assignments:
                    raise ValueError(f"Invalid preference '{pref}' for dancer {dancer.name}")
        

    def phase_1(self):
        print("Running phase 1...")

        # Create graph
        graph = nx.DiGraph()
        graph.add_node("source", demand=-self.num_dancers)
        graph.add_node("sink", demand=self.num_dancers)

        # Create nodes for dances
        for dance in self.dances:
            graph.add_node(dance.name)
            graph.add_edge(dance.name, "sink", capacity=dance.max_capacity)

        # Create nodes for dancers
        for dancer in self.dancers:
            graph.add_node(dancer.email)
            graph.add_edge("source", dancer.email, capacity=1)

            # Add edges for dancer preferences (only looking at top 3 right now)
            assert(len(dancer.preferences) >= 3)
            graph.add_edge(dancer.email, dancer.preferences[0], capacity=1, weight=1)
            graph.add_edge(dancer.email, dancer.preferences[1], capacity=1, weight=2)
            graph.add_edge(dancer.email, dancer.preferences[2], capacity=1, weight=3)

        # Run min cost flow algorithm
        matching = nx.min_cost_flow(graph)

        # Update assignments
        for dancer in self.dancers:
            for key, val in matching[dancer.email].items():
                if val == 1:
                    self.dance_assignments[key].append(dancer.email)
                    # Remove the current assignment from dancer's preferences for phase 2
                    dancer.preferences.remove(key)
    
    def phase_2(self):
        print("Running phase 2...")
    
        # Get list of dancers who requested multiple dances
        phase_2_dancers = [dancer for dancer in self.dancers if dancer.dances > 1]
        num_assignments = sum(dancer.dances - 1 for dancer in phase_2_dancers)

        # Update capacities of dances after phase 1
        for dance in self.dances:
            dance.max_capacity -= len(self.dance_assignments[dance.name])

        # Create graph
        graph = nx.DiGraph()
        graph.add_node("source", demand=-num_assignments)
        graph.add_node("sink", demand=num_assignments)

        # Create nodes for dances
        for dance in self.dances:
            graph.add_node(dance.name)
            graph.add_edge(dance.name, "sink", capacity=dance.max_capacity)

        # Create nodes for dancers
        for dancer in phase_2_dancers:
            graph.add_node(dancer.email)
            graph.add_edge("source", dancer.email, capacity=dancer.dances-1)

            # Add edges for dancer preferences
            for weight, pref in enumerate(dancer.preferences):
                graph.add_edge(dancer.email, pref, capacity=1, weight=weight+1)

        # Run min cost flow algorithm
        matching = nx.min_cost_flow(graph)
        
        # Update assignments
        for dancer in phase_2_dancers:
            for key, val in matching[dancer.email].items():
                if val == 1:
                    self.dance_assignments[key].append(dancer.email)
                    
    def phase_3(self):
        print("Running phase 3...")

        # Create graph
        graph = nx.DiGraph()
        graph.add_node("source", demand=-self.num_dancers)
        graph.add_node("sink", demand=self.num_dancers)

        # Create nodes for dances
        for dance in self.dances:
            graph.add_node(dance.name)
            graph.add_edge(dance.name, "sink", capacity=dance.max_capacity)

        # Create nodes for dancers
        for dancer in self.dancers:
            graph.add_node(dancer.email)
            graph.add_edge("source", dancer.email, capacity=dancer.dances)

            # Add edges for dancer preferences
            for rank, pref in enumerate(dancer.preferences):
                cost = rank_dict[rank+1];
                graph.add_edge(dancer.email, pref, capacity=1, weight=cost)

        # Run min cost flow algorithm
        matching = nx.min_cost_flow(graph)

        # Update assignments
        for dancer in self.dancers:
            for key, val in matching[dancer.email].items():
                if val == 1:
                    self.dance_assignments[key].append(dancer.email)

    def compute_stats(self):
        top_1_count = 0
        top_2_count = 0
        top_3_count = 0
        for dancer in self.dancers:
            for rank, pref in enumerate(dancer.preferences):
                if rank == 0 and dancer.email in self.dance_assignments[pref]:
                    top_1_count += 1
                elif rank == 1 and dancer.email in self.dance_assignments[pref]:
                    top_2_count += 1
                elif rank == 2 and dancer.email in self.dance_assignments[pref]:
                    top_3_count += 1
        
        print(f"Percentage of dancers who got their 1st choice: {top_1_count}/{self.num_dancers} ({top_1_count / self.num_dancers * 100:.2f}%)")
        print(f"Percentage of dancers who got their 2nd choice: {top_2_count}/{self.num_dancers} ({top_2_count / self.num_dancers * 100:.2f}%)")
        print(f"Percentage of dancers who got their 3rd choice: {top_3_count}/{self.num_dancers} ({top_3_count / self.num_dancers * 100:.2f}%)")

    def export_assignments(self, filename):
        print("Exporting assignments to excel...")

        # Look-up dancers from emails
        dancer_map = {}
        for dancer in self.dancers:
            dancer_map[dancer.email] = dancer
            

        # Create excel file
        with pd.ExcelWriter(filename) as writer:
            # Create master sheet with each dance as a column
            dance_list = []
            for dance_name, dancer_emails in self.dance_assignments.items():
                names = [dancer_map[e].name for e in dancer_emails]
                dance = pd.Series(names, name=dance_name.split(" (")[0])
                dance_list.append(dance)
            df = pd.concat(dance_list, axis=1)
            df.to_excel(writer, sheet_name="All Assignments", index=False)
            
            # Create a df for each dance
            for dance_name, dancer_emails in self.dance_assignments.items():
                data = [{"Dancer Name": dancer_map[e].name, "Email": dancer_map[e].email} for e in dancer_emails]
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=dance_name.split(" (")[0], index=False)

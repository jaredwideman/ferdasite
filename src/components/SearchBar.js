import React from 'react';
import { Search } from 'semantic-ui-react';
import _ from 'lodash';
// import "semantic-ui-css/semantic.min.css";


const names = [
    'Jared Wideman',
    'Connor James Gray',
    'Cody Coughlan'
];

export default class SearchBar extends React.Component {
    constructor() {
        super()
        this.state = {value: '', results: [], isLoading: false}
    }

    resetComponent = () => this.setState({ isLoading: false, results: [], value: "" });
    
    handleSearchChange = (e, { value }) => {
        this.setState({ isLoading: true, value });

        setTimeout(() => {
            if (this.state.value.length < 1) {
                this.resetComponent();
                return;
            }
            this.setState({
                isLoading: false,
                results: _.filter(names, name => {
                    return name.toLowerCase().includes(this.state.value.toLowerCase());
                })
            });
            console.log(this.state.results);
        }, 500);
    };

    handleResultSelect = (e, { result }) => {
        this.setState({ value: result });
    }

    render() {
        const { isLoading, results, value } = this.state;
        return <Search 
                    type="text"
                    loading={isLoading}
                    results={results}
                    value={value}
                    onSearchChange={this.handleSearchChange}
                    onResultSelect={this.handleResultSelect}
                />
    }
}

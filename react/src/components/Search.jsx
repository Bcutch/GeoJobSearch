import React from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const Search = () => {
  return (
    <div className="flex justify-center pt-4 bg-gray-100">
      <Form className="flex gap-2">
        <Form.Group>
          <Form.Control type="search" placeholder="Search" />
        </Form.Group>
        <Button variant="primary" type="submit">
          Find Jobs
        </Button>
      </Form>
    </div>
  );
};

export default Search;

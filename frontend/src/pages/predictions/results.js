import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';

// material-ui
import { alpha, useTheme } from '@mui/material/styles';
import {
  Box,
  Chip,
  Collapse,
  Divider,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel
} from '@mui/material';
import { visuallyHidden } from '@mui/utils';

// project-imports
import MainCard from 'components/MainCard';
import IconButton from 'components/@extended/IconButton';

// assets
import { ArrowDown2, ArrowUp2 } from 'iconsax-react';
import useAuth from 'hooks/useAuth';
import axiosServices from 'utils/axios';

function formatLocalDateFromUTC(date) {
  const year = date.getFullYear();
  const month = date.getMonth() + 1; // getMonth() returns 0-11
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();
  const pad = (num) => (num < 10 ? '0' + num : num);
  const formattedDate = `${year}-${pad(month)}-${pad(day)} ${pad(hours)}-${pad(minutes)}-${pad(seconds)}`;
  return formattedDate;
}

function Row({ row }) {
  const theme = useTheme();
  const [open, setOpen] = useState(false);
  const backColor = alpha(theme.palette.primary.lighter, 0.1);
  let date = new Date(`${row.created_time} UTC`);
  date = formatLocalDateFromUTC(date);

  return (
    <>
      <TableRow hover sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell sx={{ pl: 3 }}>
          {row.predictions != null && row.predictions.length > 0 && (
            <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
              {open ? <ArrowUp2 /> : <ArrowDown2 />}
            </IconButton>
          )}
        </TableCell>
        <TableCell component="th" scope="row">
          {row.id}
        </TableCell>
        <TableCell>{date}</TableCell>
        <TableCell>
          {row.status === 'success' && <Chip color="success" label="Success" size="small" variant="light" />}
          {row.status === 'in_progress' && <Chip color="info" label="In Progress" size="small" variant="light" />}
          {row.status === 'error' && <Chip color="error" label="Error" size="small" variant="light" />}
        </TableCell>
      </TableRow>
      <TableRow sx={{ bgcolor: backColor, '&:hover': { bgcolor: `${backColor} !important` } }}>
        <TableCell sx={{ py: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            {open && (
              <Box sx={{ py: 3, pl: { xs: 3, sm: 5, md: 6, lg: 10, xl: 12 } }}>
                <TableContainer>
                  <MainCard content={false}>
                    <Table size="small" aria-label="purchases">
                      <TableHead>
                        <TableRow>
                          <TableCell>User ID</TableCell>
                          <TableCell>Product ID</TableCell>
                          <TableCell>Quantity</TableCell>
                          <TableCell>Date</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {row.predictions?.map((pred, i) => (
                          <TableRow hover key={i}>
                            <TableCell component="th" scope="row">
                              {pred.user_id}
                            </TableCell>
                            <TableCell>{pred.product_id}</TableCell>
                            <TableCell>{pred.quantity}</TableCell>
                            <TableCell>{pred.date}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </MainCard>
                </TableContainer>
              </Box>
            )}
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

Row.propTypes = {
  row: PropTypes.shape({
    id: PropTypes.number,
    created_time: PropTypes.string,
    status: PropTypes.string,
    predictions: PropTypes.arrayOf(PropTypes.object)
  })
};

// ==============================|| Results ||============================== //

export default function Results() {
  const [results, setResults] = useState([]);
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('id');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    fetchResults();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function fetchResults() {
    try {
      let response = await axiosServices.get(`/user/${user.id}`);
      console.log(response.data.predictions);
      setResults(response.data.predictions);
    } catch (error) {
      setResults([]);
    }
    setLoading(false);
  }

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const createSortHandler = (property) => (event) => {
    handleRequestSort(event, property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event?.target.value, 10));
    setPage(0);
  };

  function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }

  function getComparator(order, orderBy) {
    return order === 'desc' ? (a, b) => descendingComparator(a, b, orderBy) : (a, b) => -descendingComparator(a, b, orderBy);
  }

  function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
  }

  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - results.length) : 0;

  if (loading) return <Skeleton animation="wave" />;

  return (
    <MainCard content={false} title="Previous Predictions">
      <TableContainer>
        <Table aria-label="collapsible table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ pl: 3 }} />
              <TableCell sortDirection={orderBy === 'id' ? order : undefined}>
                <TableSortLabel active={orderBy === 'id'} direction={orderBy === 'id' ? order : 'asc'} onClick={createSortHandler('id')}>
                  Id
                  {orderBy === 'id' ? (
                    <Box component="span" sx={visuallyHidden}>
                      {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                    </Box>
                  ) : null}
                </TableSortLabel>
              </TableCell>
              <TableCell>Created Time</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {stableSort(results, getComparator(order, orderBy))
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row) => {
                if (typeof row === 'number') return null;

                return <Row key={row.name} row={row} />;
              })}

            {emptyRows > 0 && (
              <TableRow sx={{ height: 53 * emptyRows }}>
                <TableCell colSpan={6} />
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <Divider />
      {/* table pagination */}
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={results.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </MainCard>
  );
}

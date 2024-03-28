// assets
import { PresentionChart, DocumentUpload } from 'iconsax-react';

// icons
const icons = {
  uploadCsv: DocumentUpload,
  results: PresentionChart
};

// ==============================|| MENU ITEMS - Predictions ||============================== //

const predictions = {
  id: 'group-predictions',
  title: 'Predictions',
  type: 'group',
  children: [
    {
      id: 'upload-csv',
      title: 'Upload CSV',
      type: 'item',
      url: '/predictions/upload-csv',
      icon: icons.uploadCsv
    },
    {
      id: 'results',
      title: 'Results',
      type: 'item',
      url: '/predictions/results',
      icon: icons.results
    }
  ]
};

export default predictions;
